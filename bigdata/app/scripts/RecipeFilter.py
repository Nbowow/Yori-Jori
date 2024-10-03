import difflib
import json
import re
from collections.abc import Sequence
from datetime import datetime

import pytz
from hdfs import InsecureClient
from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col, when, regexp_extract, udf
from pyspark.sql.types import StringType
from sqlalchemy import Column, BigInteger, String, Boolean, select, Integer, DateTime, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

# load_dotenv()

# KST 타임존 설정
kst = pytz.timezone('Asia/Seoul')

DATABASE_URL = "mysql+pymysql://eejuuung:eejuuung@mysql:3306/yorijori?charset=utf8mb4"


class engineconnection:

    def __init__(self):
        self.engine = create_engine(DATABASE_URL, echo=False, pool_recycle=500)

    def sessionmaker(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

    def connection(self):
        conn = self.engine.connect()

        return conn


# HDFS 클라이언트 설정 (HDFS NameNode 주소로 접속)
hdfs_client = InsecureClient('http://master:9870', user='root')
hdfs_directory = "/user/root/recipe/"

# 공통코드 (알러지 목록) 매핑 사전
allergy_code_mapping = {
    '알류': 'A_0001',
    '우유': 'A_0002',
    '메밀': 'A_0003',
    '땅콩': 'A_0004',
    '대두 (콩)': 'A_0005',
    '밀': 'A_0006',
    '잣': 'A_0007',
    '호두': 'A_0008',
    '게': 'A_0009',
    '새우': 'A_0010',
    '오징어': 'A_0011',
    '고등어': 'A_0012',
    '조개류': 'A_0013',
    '복숭아': 'A_0014',
    '토마토': 'A_0015',
    '닭고기': 'A_0016',
    '돼지고기': 'A_0017',
    '쇠고기': 'A_0018',
    '아황산류 (황산화물)': 'A_0019'
}

# 종류별 카테고리 매핑 사전
category_mapping = {
    '전체': 'B_0001',
    '밑반찬': 'B_0002',
    '메인반찬': 'B_0003',
    '국/탕': 'B_0004',
    '찌개': 'B_0005',
    '디저트': 'B_0006',
    '면/만두': 'B_0007',
    '밥/죽/떡': 'B_0008',
    '퓨전': 'B_0009',
    '김치/젓갈/장류': 'B_0010',
    '양념/소스/잼': 'B_0011',
    '양식': 'B_0012',
    '샐러드': 'B_0013',
    '스프': 'B_0014',
    '빵': 'B_0015',
    '과자': 'B_0016',
    '차/음료/술': 'B_0017',
    '기타': 'B_0018'
}

# 상황별 카테고리 매핑 사전
situation_mapping = {
    '전체': 'C_0001',
    '일상': 'C_0002',
    '초스피드': 'C_0003',
    '손님접대': 'C_0004',
    '술안주': 'C_0005',
    '다이어트': 'C_0006',
    '도시락': 'C_0007',
    '영양식': 'C_0008',
    '간식': 'C_0009',
    '야식': 'C_0010',
    '푸드스타일링': 'C_0011',
    '해장': 'C_0012',
    '명절': 'C_0013',
    '이유식': 'C_0014',
    '기타': 'C_0015'
}

# 재료별 카테고리 매핑 사전
ingredient_mapping = {
    '전체': 'D_0001',
    '소고기': 'D_0002',
    '돼지고기': 'D_0003',
    '닭고기': 'D_0004',
    '육류': 'D_0005',
    '채소류': 'D_0006',
    '해물류': 'D_0007',
    '달걀/유제품': 'D_0008',
    '가공식품류': 'D_0009',
    '쌀': 'D_0010',
    '밀가루': 'D_0011',
    '건어물류': 'D_0012',
    '버섯류': 'D_0013',
    '과일류': 'D_0014',
    '콩/견과류': 'D_0015',
    '곡류': 'D_0016',
    '기타': 'D_0017'
}

# 방법별 카테고리 매핑 사전
method_mapping = {
    '전체': 'E_0001',
    '볶음': 'E_0002',
    '끓이기': 'E_0003',
    '부침': 'E_0004',
    '조림': 'E_0005',
    '무침': 'E_0006',
    '비빔': 'E_0007',
    '찜': 'E_0008',
    '절임': 'E_0009',
    '튀김': 'E_0010',
    '삶기': 'E_0011',
    '굽기': 'E_0012',
    '데치기': 'E_0013',
    '회': 'E_0014',
    '기타': 'E_0015'
}

# 사전 정의된 매칭 규칙
material_mapping = {
    '소고기': '소고기 안심',
    '소 고기': '소고기 안심',
    '쇠고기': '소고기 안심',
    '쇠 고기': '소고기 안심',
    '돼지고기': '돼지고기 삼겹살',
    '돼지 고기': '돼지고기 삼겹살',
    # 필요시 더 많은 규칙 추가
}

# 알러지 항목에 따른 세부 품목 리스트
allergy_mapping = {
    '알류': ['달걀', '계란', '메추리알', '오리알', '거위알', '난백', '흰자', '난황', '노른자', '계란 파우더', '난백 파우더', '마요네즈', '타르타르 소스', '홀랜다이즈 소스',
           '에그누들', '팬케이크 믹스', '머랭', '크레페', '에그'],
    '우유': ['우유', '연유', '크림', '치즈', '버터', '요거트', '사워 크림', '카제인', '유청 단백질', '우유 분말'],
    '메밀': ['메밀가루', '메밀면 (소바)', '메밀빵', '메밀 크래커', '메밀 팬케이크', '메밀'],
    '땅콩': ['땅콩', '땅콩버터', '땅콩 오일', '땅콩 가루', '땅콩 소스', '땅콩 스낵'],
    '대두 (콩)': ['대두', '콩', '두부', '된장', '간장', '콩기름', '콩 단백질', '템페', '낫토', '두유', '에다마메'],
    '밀': ['밀가루', '통밀', '빵', '파스타', '크래커', '시리얼', '쿠키', '케이크', '밀가루 베이스 믹스', '밀글루텐'],
    '잣': ['잣', '잣 오일', '잣 가루', '잣 페스토'],
    '호두': ['호두', '호두 오일', '호두 가루', '호두 스낵'],
    '게': ['게', '게살', '크랩 스틱 (가공 게 제품)', '게 소스'],
    '새우': ['새우', '건새우', '새우 페이스트', '새우칩'],
    '오징어': ['오징어', '마른 오징어', '오징어볼', '오징어젓갈'],
    '고등어': ['고등어', '고등어 통조림', '훈제 고등어'],
    '조개류': ['조개', '바지락', '홍합', '가리비', '굴', '전복', '모시조개', '대합'],
    '복숭아': ['복숭아', '복숭아 잼', '복숭아 통조림', '복숭아 주스'],
    '토마토': ['토마토', '토마토 페이스트', '토마토 소스', '토마토 퓨레', '케첩'],
    '닭고기': ['닭고기', '닭가슴살', '닭날개', '닭다리', '치킨 스톡', '닭고기 소시지'],
    '돼지고기': ['돼지고기', '삼겹살', '베이컨', '햄', '소시지', '돼지갈비'],
    '쇠고기': ['쇠고기', '소고기', '스테이크', '쇠고기 소시지', '쇠고기 스톡', '쇠고기 다짐육'],
    '아황산류 (황산화물)': ['건조 과일', '와인']
}

# Spark 세션 생성
spark = SparkSession.builder \
    .appName("Filter Recipe Squash") \
    .config("spark.sql.shuffle.partitions", "50") \
    .getOrCreate()


class Users(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, autoincrement=True, index=True, nullable=False)
    user_email = Column(String(255))
    user_nickname = Column(String(255))
    user_image = Column(String(255))
    user_name = Column(String(255))
    user_score = Column(BigInteger, default=0, nullable=False)
    user_social_id = Column(String(30))
    user_social_type = Column(String(30))
    user_password = Column(String(30))
    user_refresh_token = Column(String(100))
    user_role = Column(String(30))
    user_status = Column(Boolean, default=True, nullable=False)
    created_date = Column(DateTime, default=datetime.now(kst), nullable=False)
    modified_date = Column(DateTime, default=datetime.now(kst), onupdate=datetime.now(kst), nullable=False)

    # 관계설정
    recipe = relationship("Recipes", back_populates="user")


class Materials(Base):
    __tablename__ = "materials"

    material_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    material_name = Column(String(20), nullable=False)
    material_price_status = Column(Boolean, default=False, nullable=False)
    material_img = Column(String(512))
    material_allergy_num = Column(String(20))

    recipe_materials = relationship("RecipeMaterials", back_populates="material")


class RecipeMaterials(Base):
    __tablename__ = "recipematerials"

    recipe_material_id = Column(BigInteger, primary_key=True, nullable=False, index=True, autoincrement=True)
    recipe_material_amount = Column(String(100))
    recipe_material_unit = Column(String(100))

    recipe_id = Column(BigInteger, ForeignKey("recipes.recipe_id"), nullable=False)
    recipe = relationship("Recipes", back_populates="recipe_materials")

    material_id = Column(BigInteger, ForeignKey("materials.material_id"), nullable=True)
    material = relationship("Materials", back_populates="recipe_materials")


class Recipes(Base):
    __tablename__ = "recipes"

    recipe_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    recipe_title = Column(String(255))
    recipe_name = Column(String(255))
    recipe_intro = Column(String(1024))
    recipe_image = Column(String(255))
    recipe_like_count = Column(BigInteger, default=0, nullable=False)
    recipe_view_count = Column(BigInteger, default=0, nullable=False)
    recipe_servings = Column(Integer, default=1, nullable=False)
    recipe_time = Column(Integer, default=30, nullable=False)
    recipe_level = Column(String(10), default="아무나", nullable=False)
    recipe_type = Column(String(20))
    recipe_situation = Column(String(20))
    recipe_ingredients = Column(String(20))
    recipe_method = Column(String(20))
    created_date = Column(DateTime, default=datetime.now(kst), nullable=False)
    modified_date = Column(DateTime, default=datetime.now(kst), onupdate=datetime.now(kst), nullable=False)
    user_status = Column(Boolean, default=True, nullable=False)

    user_id = Column(BigInteger, ForeignKey("users.user_id"), nullable=False)
    user = relationship("Users", back_populates="recipe")

    recipe_orders = relationship("RecipeOrders", back_populates="recipe")

    recipe_materials = relationship("RecipeMaterials", back_populates="recipe")

    # recipe_nutrient = relationship("RecipeNutrient", back_populates="recipe")


class RecipeOrders(Base):
    __tablename__ = "recipeorders"

    recipe_order_id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    recipe_order_content = Column(String(512), nullable=False)
    recipe_order_num = Column(Integer, nullable=False)
    recipe_order_img = Column(String(512))

    recipe_id = Column(BigInteger, ForeignKey("recipes.recipe_id"), nullable=False)
    recipe = relationship("Recipes", back_populates="recipe_orders")


def main():
    file_statuses = hdfs_client.list(hdfs_directory)

    print("1. hdfs 파일 목록 읽기")

    for file_name in file_statuses:
        file_path = f"hdfs://master:9870{hdfs_directory}{file_name}"

        # 파일 경로를 이용해 데이터를 정제 및 저장
        print("2. hdfs 파일 정제시작")
        process_recipe_data(file_path)

        print(f"Uploaded data from {file_name} to MySQL")

    return {"message": "All files processed and uploaded to MySQL"}


# HDFS 파일을 읽고 Spark DataFrame으로 처리하여 정제하는 함수
def process_recipe_data(file_path):
    # HDFS에서 데이터 읽기
    df = spark.read.csv(
        "hdfs://master:9000/user/root/recipe/*.csv",
        header=True,
        inferSchema=True,
        encoding='utf-8'
    )

    # Spark UDF로 각 매핑 함수 등록
    map_category_udf = udf(lambda x: map_category(x, category_mapping), StringType())
    map_situation_udf = udf(lambda x: map_category(x, situation_mapping), StringType())
    map_ingredient_udf = udf(lambda x: map_category(x, ingredient_mapping), StringType())
    map_method_udf = udf(lambda x: map_category(x, method_mapping), StringType())

    print("3. hdfs read.csv 성공")
    # 레시피이름, 글 제목, 조리순서가 null이 아닌 행만 필터링
    df = df.filter(df['레시피이름'].isNotNull() & df['글 제목'].isNotNull() & df['조리순서'].isNotNull() &
                   (df['조리순서'] != '[]'))

    # 조회수 데이터에서 콤마를 제거하고 정수형으로 변환
    df = df.withColumn("조회수", regexp_replace(col("조회수"), ",", "").cast("int"))

    # 종류별 카테고리를 코드로 변환
    df = df.withColumn("종류별", map_category_udf(col("종류별")))

    # 상황별 카테고리를 코드로 변환
    df = df.withColumn("상황별", map_situation_udf(col("상황별")))

    # 재료별 카테고리를 코드로 변환
    df = df.withColumn("재료별", map_ingredient_udf(col("재료별")))

    # 방법별 카테고리를 코드로 변환
    df = df.withColumn("방법별", map_method_udf(col("방법별")))

    # 조리시간
    df = df.withColumn(
        "조리시간",
        when(
            col("조리시간").isNull(), 60  # None 또는 null 값일 경우 60으로 고정
        ).otherwise(
            regexp_extract(col("조리시간"), r'(\d+)', 1).cast("int")  # 숫자만 추출하여 int로 변환
        )
    )

    # 인분 데이터를 숫자만 추출하고 None 또는 비어 있으면 1로 설정
    df = df.withColumn("인분", when(col("인분").isNull() | (col("인분") == ""), 1)
                       .otherwise(regexp_extract(col("인분"), r'(\d+)', 1).cast("int")))

    print("4. 유저클래스 먼저 넣기 아이디는 모두의 레시피")
    save_user_to_db()

    print("5. 재료, 조리순서 db 추가")
    # 재료, 조리순서 컬럼 db데이터 추가
    for row in df.collect():
        print("6. 레시피 저장")
        recipe_id = save_recipe_to_db(row)  # 레시피 저장 함수, 각 레시피에 대해 recipe_id 반환

        print("7. 레시피 재료 저장")
        process_recipe_ingredients(row['재료'], recipe_id)

        # 레시피 단계별 정보 저장
        print("8. 레시피 주문 저장")
        try:
            # JSON 형태의 문자열을 파이썬 리스트로 변환
            recipe_orders = json.loads(row['조리순서'].replace("'", '"'))
            process_recipe_orders(recipe_orders, recipe_id)
        except json.JSONDecodeError as e:
            print(f"조리순서 데이터를 처리하는 중 오류 발생: {str(e)}")


def map_category(value, mapping):
    return mapping.get(value, "기타")


def save_user_to_db():
    engine = engineconnection()
    session = engine.sessionmaker()

    # 먼저 user_id=1인 관리자가 존재하는지 확인
    existing_user = session.query(Users).filter_by(user_id=1).first()

    if existing_user:
        print("관리자 계정이 이미 존재합니다.")
    else:
        # 새 관리자 사용자 생성
        new_user = Users(
            user_id=1,
            user_email="admin@example.com",
            user_nickname="요리조리",
            user_image=None,  # 필요에 따라 설정
            user_name="Admin User",
            user_score=0,
            user_social_id=None,  # 필요에 따라 설정
            user_social_type=None,  # 필요에 따라 설정
            user_password="securepassword",  # 실제 사용 시 해시된 비밀번호 사용
            user_refresh_token=None,  # 필요에 따라 설정
            user_role="admin",
            user_status=True,
            created_date=datetime.now(kst),
            modified_date=datetime.now(kst)
        )

        # 데이터베이스에 추가
        session.add(new_user)

        # 변경 사항 커밋
        session.commit()

        print("새 관리자 사용자가 추가되었습니다.")

    # 세션 닫기
    session.close()


def save_recipe_to_db(row):
    engine = engineconnection()
    session = engine.sessionmaker()

    # 중복 확인을 위해 기존 레시피 확인 (예: 레시피 이름과 제목을 기준으로 중복 확인)
    existing_recipe = session.query(Recipes).filter(
        Recipes.recipe_id == row['index'],
        Recipes.recipe_name == row['레시피이름'],
        Recipes.recipe_title == row['글 제목']
    ).first()

    if existing_recipe:
        print(f"이미 존재하는 레시피입니다: {existing_recipe.recipe_id}")
        return existing_recipe.recipe_id  # 중복된 레시피의 ID 반환

    # 'row'를 딕셔너리로 변환
    row_dict = row.asDict()
    print(f"레시피 이름: {row_dict['레시피이름']}")

    # recipe_id가 올바른 값인지 확인
    try:
        recipe_id_value = int(row_dict['index'])  # recipe_id는 정수형이어야 함
    except ValueError as e:
        print(f"recipe_id 변환 오류: {e} - 원래 값: {row_dict['index']}")
        return None  # 오류 시 None 반환

    # recipe_intro 길이 제한 (예: 500자로 제한)
    recipe_intro = row_dict['소개글']
    if recipe_intro is None:  # None 체크
        recipe_intro = ''  # None인 경우 빈 문자열로 설정
    elif len(recipe_intro) > 1000:  # 500자로 제한
        recipe_intro = recipe_intro[:1000] + '...'

    new_recipe = Recipes(
        recipe_id=recipe_id_value,
        recipe_title=row_dict['글 제목'],
        recipe_name=row_dict['레시피이름'],
        recipe_image=row_dict['레시피이미지'],
        recipe_intro=recipe_intro,
        recipe_view_count=row_dict['조회수'],
        recipe_time=row_dict['조리시간'],
        recipe_level=row_dict['난이도'],
        recipe_servings=row_dict['인분'],
        recipe_type=row_dict['종류별'],
        recipe_situation=row_dict['상황별'],
        recipe_ingredients=row_dict['재료별'],
        recipe_method=row_dict['방법별'],

        # row에 없는 값들에 기본값 설정
        user_status=row_dict.get('user_status', True),  # 사용자 상태 기본값 True
        user_id=row_dict.get('user_id', 1)  # 기본 사용자 ID 설정 (예: 1번 사용자)
    )

    session.add(new_recipe)
    session.commit()

    print(f"레시피 저장 완료: {new_recipe.recipe_id}")
    return new_recipe.recipe_id  # 저장된 레시피의 ID 반환


# 레시피 단계를 처리하고 RecipeOrders 테이블에 저장하는 함수
def process_recipe_orders(recipe_orders, recipe_id):
    """
    레시피 단계별 정보를 RecipeOrders 테이블에 저장하는 함수
    """
    if isinstance(recipe_orders, list):
        for order in recipe_orders:
            try:
                step_number = order.get('step_number')
                description = order.get('description')
                image_url = order.get('image_url')

                # 단계가 제대로 전달되지 않은 경우 무시
                if step_number is None or description is None:
                    print(f"잘못된 레시피 단계 정보: {order}")
                    continue

                # RecipeOrders 테이블에 단계 정보 저장
                add_recipe_order(recipe_id, step_number, description, image_url)

            except Exception as e:
                print(f"레시피 단계를 저장하는 중 오류 발생: {str(e)}")
                continue
    else:
        print("레시피 단계 데이터가 리스트 형태가 아닙니다.")


# RecipeOrders 테이블에 단계를 추가하는 함수
def add_recipe_order(recipe_id, step_number, description, image_url):
    """
    RecipeOrders 테이블에 단계를 추가하는 함수
    """
    engine = engineconnection()
    session = engine.sessionmaker()

    new_recipe_order = RecipeOrders(
        recipe_order_num=step_number,
        recipe_order_content=description,
        recipe_order_img=image_url,
        recipe_id=recipe_id
    )

    session.add(new_recipe_order)
    session.commit()
    # print(f"레시피 ID {recipe_id}의 단계 {step_number} 저장 완료.")


def process_recipe_ingredients(ingredients_str, recipe_id):
    """
    재료 문자열을 처리하여 RecipeMaterials 테이블에 각 재료 정보를 저장하는 함수
    """

    if not ingredients_str:  # ingredients_str가 None 또는 빈 문자열인 경우
        print("재료 문자열이 비어있거나 None입니다.")
        return

    try:
        # 문자열을 튜플 리스트로 변환
        ingredients_list = parse_ingredients(ingredients_str)

        for item in ingredients_list:
            try:
                # item이 리스트인지 확인
                if isinstance(item, tuple) and len(item) == 2:
                    material, amount_with_unit = item  # 재료명과 양 분리
                else:
                    print(f"유효하지 않은 재료 형식: {item}")
                    continue

                # 제어 문자 제거 및 공백 제거
                material = material.replace('\u200b', '').strip()
                amount_with_unit = amount_with_unit.replace('\u200b', '').strip()

                if not material:
                    continue

                # amount_with_unit이 빈 문자열인 경우 양과 단위를 추출하지 않음
                if amount_with_unit:
                    # 양과 단위를 분리 (숫자와 단위 추출)
                    amount, unit = extract_amount_and_unit(amount_with_unit)
                else:
                    amount, unit = "", ""  # 양과 단위를 None으로 설정

                # 재료 ID 확인 또는 추가
                material_info = get_material_id(material)
                material_id = material_info['material_id']

                # RecipeMaterials 테이블에 재료 저장
                add_recipe_material(recipe_id, material_id, amount, unit)

            except ValueError as e:
                print(f"재료 데이터 처리 중 오류 발생: {item}, 오류 메시지: {str(e)}")
                continue
            except Exception as e:
                print(f"예기치 못한 오류 발생: {str(e)}")
                continue

    except Exception as e:
        print(f"재료 데이터 문자열 처리 중 오류 발생: {str(e)}")


def parse_ingredients(ingredients_str):
    """
    재료 문자열을 튜플 리스트로 변환하는 함수
    """
    # 정규식을 사용하여 재료 데이터를 추출
    pattern = re.compile(r"\('([^']*)',\s*'([^']*)'\)")
    matches = pattern.findall(ingredients_str)

    # 튜플 리스트로 변환
    ingredients_list = []
    for material, amount in matches:
        # '생략 가능' 문구 제거
        material = material.replace('생략 가능', '').strip()
        amount = amount.replace('생략 가능', '').strip()
        ingredients_list.append((material, amount))

    return ingredients_list


def extract_amount_and_unit(amount_with_unit):
    """
    양과 단위를 분리하는 함수 (예: '600g'에서 '600'과 'g'를 분리)
    범위 표현과 '/'를 포함한 양을 처리하고 '조금' 같은 경우에 대한 처리를 추가
    """
    # 정규 표현식 수정: 숫자 + 범위 (예: 1.4~1.5), 단위 포함, / 처리
    match = re.match(r"([\d./~]+)([a-zA-Z]+)", amount_with_unit)

    if match:
        return match.group(1), match.group(2)  # 숫자(양)와 단위 반환
    elif '조금' in amount_with_unit:
        return '조금', ''  # '조금'인 경우 양으로 처리
    else:
        return amount_with_unit, ''  # 단위가 없으면 빈 문자열 반환


def add_recipe_material(recipe_id, material_id, amount, unit):
    """
    RecipeMaterials 테이블에 재료 정보를 추가하는 함수
    """
    engine = engineconnection()
    session = engine.sessionmaker()

    try:
        new_recipe_material = RecipeMaterials(
            recipe_material_amount=amount,
            recipe_material_unit=unit,
            recipe_id=recipe_id,  # 외부 키로 연결
            material_id=material_id
        )

        session.add(new_recipe_material)
        session.commit()
        # print(f"레시피 ID {recipe_id}에 재료 ID {material_id} 추가 완료.")

    except Exception as e:
        session.rollback()  # 오류 발생 시 트랜잭션 롤백
        print(f"레시피 재료 추가 중 오류 발생: {str(e)}")

    finally:
        session.close()


# 유사도 계산 함수
def get_best_allergy_match(item_name, reference_names, match_value):
    # '생략 가능' 문자열 제거
    cleaned_item_name = item_name.replace('생략 가능', '').strip()

    match = difflib.get_close_matches(cleaned_item_name, reference_names, n=1,
                                      cutoff=match_value)
    if match:
        return match[0]
    return item_name


def get_best_material_match(item_name, reference_names, match_value):
    # '생략 가능' 문자열 제거
    cleaned_item_name = item_name.replace('생략 가능', '').strip()

    cleaned_reference_names = [name.replace('생략 가능', '').strip() for name in reference_names]

    match = difflib.get_close_matches(cleaned_item_name, cleaned_reference_names, n=1,
                                      cutoff=match_value)
    if match:
        return match[0]
    return item_name


# 재료가 알레르기 항목에 해당하는지 확인하는 함수
def get_allergy_num(material_name):
    for allergy_category, items in allergy_mapping.items():
        best_match = get_best_allergy_match(material_name, items, 0.8)

        if best_match != material_name:
            print(f"'{material_name}'이(가) '{best_match}' 항목으로 매칭되었습니다. 알레르기 카테고리: {allergy_category}")
            allergy_code = allergy_code_mapping.get(allergy_category)

            if allergy_code:
                return allergy_code  # 알레르기 공통 코드 반환
            else:
                print(f"'{allergy_category}'에 대한 알레르기 코드가 존재하지 않습니다.")

    return ""  # 알레르기 코드가 없는 경우 None 반환


def get_material_id(material_name):
    # 재료 존재여부 확인하고 테이블 추가
    engine = engineconnection()
    session = engine.sessionmaker()

    try:
        print(f"입력된 재료명: '{material_name}'")  # 입력된 재료명 확인

        # 기존 재료 리스트 추출 (재료 이름 리스트)
        stmt_reference = select(Materials.material_name)
        reference_materials: Sequence[str] = session.execute(stmt_reference).scalars().all()  # Sequence로 변경

        # 참조 재료 리스트가 비어 있는 경우 바로 새로운 재료 추가
        if not reference_materials:
            allergy_num = get_allergy_num(material_name)
            print(f"참조 재료 리스트가 비어 있습니다. 새 재료 추가: '{material_name}', 알레르기 번호: {allergy_num}")  # 추가될 재료 정보 확인
            new_material = Materials(
                material_name=material_name,
                material_allergy_num=allergy_num  # 알레르기 번호 추가
            )
            session.add(new_material)
            session.commit()  # 새로운 재료를 데이터베이스에 추가
            print(f"'{material_name}' 재료가 추가되었습니다. 새로운 ID: {new_material.material_id}")  # 추가 확인
            return {"material_id": new_material.material_id, "material_name": new_material.material_name}

        # 재료명 유사도 계산하여 가장 유사한 이름 반환
        best_match = get_best_material_match(material_name, reference_materials, 0.85)

        print(f"최고 매칭 재료명: '{best_match}'")  # 매칭된 재료명 확인

        # 유사도가 높은 재료가 있는지 확인
        if best_match != material_name:
            print(f"'{material_name}'이(가) '{best_match}'으로 매칭되었습니다.")
            material_name = best_match  # 유사한 값으로 재료명 변경

        # 재료가 존재하는지 확인하는 쿼리
        stmt = select(Materials).where(Materials.material_name == material_name)

        # 쿼리 실행
        material = session.execute(stmt).scalars().first()

        if material:
            print(f"'{material_name}'이(가) 이미 존재합니다. ID: {material.material_id}")
            return {"material_id": material.material_id, "material_name": material.material_name}
        else:
            # 재료가 없다면 새로운 재료 추가 (material_id는 auto increment로 자동 처리)
            allergy_num = get_allergy_num(material_name)
            print(f"새 재료 추가: '{material_name}', 알레르기 번호: {allergy_num}")  # 추가될 재료 정보 확인
            new_material = Materials(
                material_name=material_name,
                material_allergy_num=allergy_num  # 알레르기 번호 추가
            )
            session.add(new_material)
            session.commit()  # 새로운 재료를 데이터베이스에 추가
            print(f"'{material_name}' 재료가 추가되었습니다. 새로운 ID: {new_material.material_id}")  # 추가 확인
            return {"material_id": new_material.material_id, "material_name": new_material.material_name}
    except Exception as e:
        session.rollback()  # 오류 발생 시 트랜잭션 롤백
        print(f"재료 처리 중 오류 발생: {str(e)}")
    finally:
        session.close()


if __name__ == "__main__":
    main()
