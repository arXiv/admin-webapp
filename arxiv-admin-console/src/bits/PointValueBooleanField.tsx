import React from 'react';
import { BooleanField, BooleanFieldProps, useRecordContext } from 'react-admin';

interface PointValueBooleanFieldProps extends BooleanFieldProps {
    record?: any;
}

const PointValueBooleanField: React.FC<PointValueBooleanFieldProps> = (props) => {
    const record = useRecordContext();
    const { source } = props;
    console.log(JSON.stringify(props))
    if (!record || !source) return null;
    const isOpen = record[source] === 0;
    const customRecord = { ...record, [source]: isOpen};
    console.log(`${record[source]} open ${isOpen}`)
    return (<BooleanField {...props} record={customRecord} />);
};

export default PointValueBooleanField;
