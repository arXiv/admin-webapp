import { useMediaQuery } from '@mui/material';
import {
    List,
    SimpleList,
    Datagrid,
    TextField,
    EmailField,
    BooleanField,
    SortPayload,
    NumberInput,
    useRecordContext,
    Edit,
    SimpleForm,
    TextInput,
    ReferenceInput,
    Create,
    Filter,
    BooleanInput,
    DateField,
    ReferenceField,
    NumberField,
    DateInput, useListContext, SelectInput,
    AutocompleteArrayInput
} from 'react-admin';

import LinkIcon from '@mui/icons-material/Link';


import { addDays } from 'date-fns';

import React from "react";

const presetOptions = [
    { id: 'last_1_day', name: 'Last 1 Day' },
    { id: 'last_7_days', name: 'Last 7 Days' },
    { id: 'last_28_days', name: 'Last 28 Days' },
];

const calculatePresetDates = (preset: string) => {
    const today = new Date();
    switch (preset) {
        case 'last_1_day':
            return { startDate: addDays(today, -1), endDate: today };
        case 'last_7_days':
            return { startDate: addDays(today, -7), endDate: today };
        case 'last_28_days':
            return { startDate: addDays(today, -28), endDate: today };
        default:
            return { startDate: null, endDate: null };
    }
};

const SubmissionFilter = (props: any) => {
    const { setFilters, filterValues } = useListContext();
    const handlePresetChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        const { startDate, endDate } = calculatePresetDates(event.target.value);
        setFilters({
            ...filterValues,
            startDate: startDate ? startDate.toISOString().split('T')[0] : '',
            endDate: endDate ? endDate.toISOString().split('T')[0] : '',
        });
    };

    const statusChoices = [
        { id: 1, name: 'Status 1' },
        { id: 2, name: 'Status 2' },
        { id: 3, name: 'Status 3' },
        { id: 4, name: 'Status 4' },
        { id: 5, name: 'Status 5' },
    ];


    return (
        <Filter {...props}>
            <SelectInput
                label="Preset Date Range"
                source="preset"
                choices={presetOptions}
                onChange={(event) => handlePresetChange(event as React.ChangeEvent<HTMLSelectElement>)}
                alwaysOn
            />
            <DateInput label="Start Date" source="start_date" />
            <DateInput label="End Date" source="end_date" />
            <BooleanInput label="Valid" source="flag_valid" />

            <AutocompleteArrayInput
                label="Status"
                source="status"
                choices={statusChoices}
                optionText="name"
                optionValue="id"
            />
        </Filter>
    );
};


export const SubmissionList = () => {
    const sorter: SortPayload = {field: 'submission_id', order: 'ASC'};
    const isSmall = useMediaQuery<any>(theme => theme.breakpoints.down('sm'));
    return (
        <List filters={<SubmissionFilter />}>
            {isSmall ? (
                <SimpleList
                    primaryText={record => record.name}
                    secondaryText={record => record.submissionname}
                    tertiaryText={record => record.email}
                />
            ) : (
                <Datagrid rowClick="edit" sort={sorter}>
                    <NumberField source="id" label="Submission ID" />
                    <TextField source="title" />
                    <ReferenceField source="document_id" reference="documents" label={"Document"}
                                    link={(record, reference) => `/${reference}/${record.id}`} >
                        <LinkIcon />
                    </ReferenceField>
                    <ReferenceField source="submitter_id" reference="users" label={"Submitter"}
                                    link={(record, reference) => `/${reference}/${record.id}`} >
                        <TextField source={"last_name"} />
                        {", "}
                        <TextField source={"first_name"} />
                    </ReferenceField>
                    <DateField source="submit_time" label={"When"}/>
                </Datagrid>
            )}
        </List>
    );
};


const SubmissionTitle = () => {
    const record = useRecordContext();
    return <span>Submission {record ? `"${record.last_name}, ${record.first_name}" - ${record.email}` : ''}</span>;
};

export const SubmissionEdit = () => (
    <Edit title={<SubmissionTitle />}>
        <SimpleForm>
            <ReferenceField source="endorsee_id" reference="users" label={"Endorsee"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <TextField source={"last_name"} />
                {", "}
                <TextField source={"first_name"} />
            </ReferenceField>

            <ReferenceField source="endorser_id" reference="users" label={"Endorser"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <TextField source={"last_name"} />
                {", "}
                <TextField source={"first_name"} />
            </ReferenceField>

            <TextInput source="archive" />

            <TextInput source="subject_class" />
            <BooleanInput source="flag_valid" label={"Valid"} />

            <TextInput source="type" />
            <NumberInput source="point_value" label={"Point"} />
            <DateInput source="issued_when" label={"Issued"} />

            <ReferenceField source="request_id" reference="submission_request" label={"Request"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
            </ReferenceField>
        </SimpleForm>
    </Edit>
);

export const SubmissionCreate = () => (
    <Create>
        <SimpleForm>
            <ReferenceField source="endorsee_id" reference="users" label={"Endorsee"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <TextField source={"last_name"} />
                {", "}
                <TextField source={"first_name"} />
            </ReferenceField>

            <ReferenceField source="endorser_id" reference="users" label={"Endorser"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <TextField source={"last_name"} />
                {", "}
                <TextField source={"first_name"} />
            </ReferenceField>

            <TextInput source="archive" />

            <TextInput source="subject_class" />
            <BooleanInput source="flag_valid" label={"Valid"}/>

            <TextInput source="type" />
            <NumberInput source="point_value" label={"Point"} />
            <DateInput source="issued_when" label={"Issued"} />

        </SimpleForm>
    </Create>
);


