import {Grid, useMediaQuery} from '@mui/material';
import {
    BooleanField,
    BooleanInput,
    Create,
    Datagrid,
    DateField,
    DateInput,
    Edit,
    EmailField,
    Filter,
    List,
    NumberField,
    NumberInput,
    ReferenceField,
    ReferenceInput,
    SelectInput,
    SimpleForm,
    SimpleList,
    SortPayload,
    TextField,
    TextInput,
    useListContext,
    useRecordContext,
} from 'react-admin';


import LinkIcon from '@mui/icons-material/Link';


import { addDays } from 'date-fns';

import React from "react";
import SubmissionStateField, {submissionStatusOptions} from "./bits/SubmissionStateField";

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

            <SelectInput
                label="Status"
                source="status"
                choices={submissionStatusOptions}
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
                    <SubmissionStateField source="status"/>
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
    <Edit>
        <SimpleForm>
            <TextField source="id" />
            <ReferenceField source="document_id" reference="documents" label={"Document"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <LinkIcon>Document</LinkIcon>
            </ReferenceField>
            <TextField source="doc_paper_id" label="Paper ID" />
            <ReferenceInput source="sword_id" reference="swords" />
            <NumberInput source="userinfo" />
            <BooleanInput source="is_author" />
            <NumberInput source="agree_policy" />
            <BooleanInput source="viewed" />
            <NumberInput source="stage" />
            <ReferenceField source="submitter_id" reference="users" label={"Submitter"}
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <TextField source={"last_name"} />
                {", "}
                <TextField source={"first_name"} />
            </ReferenceField>
            <TextInput source="submitter_name" />
            <TextInput source="submitter_email" />
            <Grid>
                {"Created: "}
            <DateField source="created" label="Created"/>
                {", Updated: "}
            <DateField source="updated" />
            </Grid>
            <SelectInput source="status" choices={submissionStatusOptions} />
            <TextInput source="sticky_status" />
            <DateInput source="must_process" />
            <DateInput source="submit_time" />
            <TextInput source="release_time" />
            <NumberInput source="source_size" />
            <TextInput source="source_format" />
            <TextInput source="source_flags" />
            <DateInput source="has_pilot_data" />
            <DateInput source="is_withdrawn" />
            <TextInput source="title" />
            <TextInput source="authors" />
            <TextInput source="comments" />
            <TextInput source="proxy" />
            <TextInput source="report_num" />
            <TextInput source="msc_class" />
            <TextInput source="acm_class" />
            <TextInput source="journal_ref" />
            <TextInput source="doi" />
            <TextInput source="abstract" />
            <TextInput source="license" />
            <NumberInput source="version" />
            <TextInput source="type" />
            <TextInput source="is_ok" />
            <TextInput source="admin_ok" />
            <DateInput source="allow_tex_produced" />
            <TextInput source="is_oversize" />
            <DateInput source="remote_addr" />
            <DateInput source="remote_host" />
            <TextInput source="package" />
            <ReferenceInput source="rt_ticket_id" reference="rt_tickets" />
            <DateInput source="auto_hold" />
            <DateInput source="is_locked" />
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


