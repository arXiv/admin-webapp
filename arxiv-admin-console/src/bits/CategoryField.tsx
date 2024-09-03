
import React from 'react';
import { useRecordContext, FieldProps } from 'react-admin';

interface CategoryFieldProps extends FieldProps {
    sourceCategory: string;
    sourceClass: string;
}

const CategoryField: React.FC<CategoryFieldProps> = ({ sourceCategory, sourceClass }) => {
    const record = useRecordContext<{ [key: string]: string }>();

    if (!record) return null;
    console.log("CategoryField:", JSON.stringify(record));

    return (
        <span>
            {record[sourceCategory]}{"."}{record[sourceClass] || '*'}
        </span>
    );
};

export default CategoryField;