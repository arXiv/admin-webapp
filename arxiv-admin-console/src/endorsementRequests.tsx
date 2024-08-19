import React, {useState, useEffect} from 'react';

import { useMediaQuery } from '@mui/material';
import {
    useDataProvider,
    List,
    SimpleList,
    Datagrid,
    TextField,
    EmailField,
    BooleanField,
    DateField,
    NumberField,
    SortPayload,
    useRecordContext,
    Edit,
    SimpleForm,
    TextInput,
    ReferenceInput,
    Create,
    Filter,
    BooleanInput,
    DateInput,
    SelectInput,
    useListContext,
    ReferenceField,
    NumberInput,
    Show,
    SimpleShowLayout, useGetOne,
} from 'react-admin';

import { addDays } from 'date-fns';

interface Category {
    id: string;
    name: string;
    description: string;
}

interface CategorySubject {
    id: string;
    name: string;
    description: string;
}

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


const EndorsementRequestFilter = (props: any) => {
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
        </Filter>
    );
};


export const EndorsementRequestList = () => {
    const sorter: SortPayload = {field: 'endorsementRequest_id', order: 'ASC'};
    const isSmall = useMediaQuery<any>(theme => theme.breakpoints.down('sm'));
    return (
        <List filters={<EndorsementRequestFilter />}>
            {isSmall ? (
                <SimpleList
                    primaryText={record => record.name}
                    secondaryText={record => record.endorsementRequestname}
                    tertiaryText={record => record.email}
                />
            ) : (
                <Datagrid rowClick="show" sort={sorter}>
                    <BooleanField source="flag_valid" label={"Valid"} FalseIcon={null} />
                    <TextField source="archive" label={"Category"}/>
                    <TextField source="subject_class" label={"Class"}/>
                    <TextField source="arXiv_categories" label={"Categories"}/>
                    <DateField source="issued_when" label={"Issued"}/>
                    <NumberField source="point_value" label={"Point"}/>
                    <ReferenceField source="endorsee_id" reference="users"
                                    link={(record, reference) => `/${reference}/${record.id}`} >
                        <TextField source={"last_name"} />
                        {", "}
                        <TextField source={"first_name"} />
                    </ReferenceField>
                </Datagrid>
            )}
        </List>
    );
};


const EndorsementRequestTitle = () => {
    const record = useRecordContext();

    // Fetch the user data based on user_id from the record
    const { data: user, isLoading } = useGetOne('users', { id: record?.endorsee_id });

    if (!record) {
        return <span>Endorsement Request - no record</span>;
    }

    if (isLoading) {
        return <span>Endorsement Request - Loading endorsee...</span>;
    }

    return (
        <span>
            Endorsement Request {user ? `"${user.last_name}, ${user.first_name}" - ${user.email}` : ''}
        </span>
    );
};

export const EndorsementRequestEdit = () => {
    const [categoryChoices, setCategoryChoices] = useState<Category[]>([]);
    const [categoryChoice, setCategoryChoice] = useState<Category>();
    const [subjectChoices, setSubjectChoices] = useState<CategorySubject[]>([]);

    const dataProvider = useDataProvider();

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const { data } = await dataProvider.getList<Category>('categories', {
                    filter: {},
                    sort: { field: 'name', order: 'ASC' },
                });
                setCategoryChoices(data);
            } catch (error) {
                console.error("Error fetching categories:", error);
            }
        };

        fetchCategories();
    }, [dataProvider]);

    useEffect(() => {
        if (categoryChoice?.id) {

            dataProvider.getList<CategorySubject>('subject_class', {
                filter: {archive: categoryChoice.id},
                sort: {field: 'name', order: 'ASC'},
            }).then(result => {
                console.log("subject_class: " + result);
                setSubjectChoices(result.data);
            });
        }
    }, [dataProvider, categoryChoice]);

    const handleCategoryChange = async (event: React.ChangeEvent<HTMLSelectElement>) => {
        const categoryId = event.target.value;
        setCategoryChoice(categoryChoices.find((c) => c.id === categoryId));
    };

    return (
        <Edit title={<EndorsementRequestTitle />}>
            <SimpleForm>
                <TextInput source="id" disabled />
                <ReferenceField source="endorsee_id" reference="users"
                                link={(record, reference) => `/${reference}/${record.id}`} >
                    <TextField source={"last_name"} fontStyle={{fontSize: '1rem'}} />
                    {", "}
                    <TextField source={"first_name"} fontStyle={{fontSize: '1rem'}} />
                </ReferenceField>

                <ReferenceInput source="endorser_id" reference="users">
                    <TextField source={"last_name"} fontStyle={{fontSize: '1rem'}} />
                    {", "}
                    <TextField source={"first_name"} fontStyle={{fontSize: '1rem'}} />
                </ReferenceInput>


                <SelectInput source="archive" label="Category" choices={categoryChoices} onChange={(event) => handleCategoryChange(event as React.ChangeEvent<HTMLSelectElement>)}/>
                <SelectInput source="subject_class" label="Subject" choices={subjectChoices} />

                <DateInput source="issued_when" disabled label={"Issued"}/>
                <NumberInput source="point_value"  label={"Point"} />
            </SimpleForm>
        </Edit>
    );
}

export const EndorsementRequestCreate = () => (
    <Create>
        <SimpleForm>
            <ReferenceInput source="endorsementRequestname" reference="endorsementRequests" />
            <TextInput source="first_name" />
            <TextInput source="last_name" />
            <TextInput source="email" />
        </SimpleForm>
    </Create>
);


export const EndorsementRequestShow = () => (
    <Show>
        <SimpleShowLayout>
            <TextField source="id" />
            <ReferenceField source="endorsee_id" reference="users"
                            link={(record, reference) => `/${reference}/${record.id}`} >
                <TextField source={"last_name"} />
                {", "}
                <TextField source={"first_name"} />
            </ReferenceField>
            <TextField source="archive" />
            <TextField source="subject_class" />
            <BooleanField source="flag_valid" />
            <DateField source="issued_when" />
            <NumberField source="point_value" />
            <BooleanField source="flag_suspect" />
            <TextField source="arXiv_categories" />
        </SimpleShowLayout>
    </Show>
);
