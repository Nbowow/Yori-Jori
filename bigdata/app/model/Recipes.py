from datetime import datetime

from sqlalchemy import BigInteger, Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database.config import Base


class Recipes(Base):
    __tablename__ = "Recipes"

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
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    modified_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    user_status = Column(Boolean, default=True, nullable=False)

    user_id = Column(BigInteger, ForeignKey("Users.user_id"), nullable=False)

    user = relationship("Users", back_populates="recipe")
