import PropTypes from "prop-types";
import { useTable } from "react-table";
import * as S from "./Table.styled";

const Table = ({ columns, data }) => {
    const { getTableProps, getTableBodyProps, headerGroups, rows, prepareRow } =
        useTable({ columns, data });

    return (
        <S.TableSheet {...getTableProps()}>
            <S.TableHead>
                {headerGroups.map((headerGroup, i) => (
                    <S.Header key={i} {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map((column, j) => (
                            <S.Th key={j} {...column.getHeaderProps()}>
                                {column.render("Header")}
                            </S.Th>
                        ))}
                    </S.Header>
                ))}
            </S.TableHead>
            <S.Tbody {...getTableBodyProps()}>
                {rows.map((row, rowIndex) => {
                    prepareRow(row);
                    return (
                        <S.Tr key={rowIndex} {...row.getRowProps()}>
                            {row.cells.map((cell, cellIndex) => (
                                <S.Td key={cellIndex} {...cell.getCellProps()}>
                                    {cell.render("Cell")}
                                </S.Td>
                            ))}
                        </S.Tr>
                    );
                })}
            </S.Tbody>
        </S.TableSheet>
    );
};

Table.propTypes = {
    columns: PropTypes.arrayOf(PropTypes.object).isRequired,
    data: PropTypes.arrayOf(PropTypes.object).isRequired,
    cell: PropTypes.shape({
        value: PropTypes.any,
    }),
};

export default Table;