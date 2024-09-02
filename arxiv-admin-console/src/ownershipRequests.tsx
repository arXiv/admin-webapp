import React, {useState, useEffect} from 'react';

import {
    Card,
    CardContent,
    CardHeader,
    Grid,
    Table,
    TableCell,
    TableRow,
    TableHead,
    useMediaQuery,
    Box,
    Typography,
    TablePagination,
    Tooltip
} from '@mui/material';

import YesIcon from '@mui/icons-material/Check';

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
    ToggleThemeButton,
    useListContext,
    ReferenceField,
    NumberInput,
    Show,
    SimpleShowLayout,
    useGetOne, RadioButtonGroupInput,
    RecordContextProvider,
    ListContextProvider,
    SourceContextProvider
} from 'react-admin';

import { addDays } from 'date-fns';
import {json} from "node:stream/consumers";

const workflowStatus = [
    { id: 'pending', name: 'Pending' },
    { id: 'accepted', name: 'Accepted' },
    { id: 'rejected', name: 'Rejected' },
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


const OwnershipRequestFilter = (props: any) => {
    const { setFilters, filterValues } = useListContext();

    const handleWorkflowStatusChoice = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setFilters({
            ...filterValues,
        });
    };

    return (
        <Filter {...props}>
            <SelectInput
                label="Workflow Status"
                source="workflow_status"
                choices={workflowStatus}
                onChange={(event) => handleWorkflowStatusChoice(event as React.ChangeEvent<HTMLSelectElement>)}
                alwaysOn
            />
        </Filter>
    );
};


export const OwnershipRequestList = () => {
    const sorter: SortPayload = {field: 'ownershipRequest_id', order: 'ASC'};
    const isSmall = useMediaQuery<any>(theme => theme.breakpoints.down('sm'));
    return (
        <List filters={<OwnershipRequestFilter />} filterDefaultValues={{workflow_status: "pending"}}>
            {isSmall ? (
                <SimpleList
                    primaryText={record => record.name}
                    secondaryText={record => record.ownershipRequestname}
                    tertiaryText={record => record.email}
                />
            ) : (
                <Datagrid rowClick="edit" sort={sorter}>
                    <NumberField source="id" label={"Request ID"}/>
                    <ReferenceField source="user_id" reference="users"
                                    link={(record, reference) => `/${reference}/${record.id}`} >
                        <TextField source={"last_name"} />
                        {", "}
                        <TextField source={"first_name"} />
                    </ReferenceField>
                    <ReferenceField source="endorsement_request_id" reference="endorsement_requests" label={"Endorsement Request"}>

                    </ReferenceField>
                    <TextField source="workflow_status" label={"Status"}/>
                    <ReferenceField source="id" reference="ownership_requests_audit" label={"Audit"}>
                        {"Remote host: "}
                        <TextField source={"remote_host"} defaultValue={"Unknown"}/>
                        {"Date: "}
                        <DateField source={"date"} />
                    </ReferenceField>

                </Datagrid>
            )}
        </List>
    );
};


const OwnershipRequestTitle = () => {
    const record = useRecordContext();

    // Fetch the ownership request data
    const { data: ownershipRequestData, isLoading: isLoadingOwnershipRequest } = useGetOne('ownership_requests', { id: record?.id });

    // Fetch the user data based on user_id from the ownership request
    const { data: userData, isLoading: isLoadingUser } = useGetOne('users', { id: ownershipRequestData?.user_id }, { enabled: !!ownershipRequestData?.user_id });

    if (!record) {
        return <span>Ownership Request - no record</span>;
    }

    if (isLoadingOwnershipRequest || isLoadingUser) {
        return <span>Ownership Request - Loading...</span>;
    }

    return (
        <span>
            Ownership Request {ownershipRequestData ? `"${ownershipRequestData.id}, ${userData?.first_name || ''}" - ${userData?.email}` : ''}
        </span>
    );
};

interface OwnershipModel {
    document_id: number;
    user_id: number;
    date: string;
    added_by: number;
    remote_addr: string;
    remote_host: string;
    tracking_cookie: string;
    valid: boolean;
    flag_author: boolean;
    flag_auto: boolean;
}

const PaperOwnerList: React.FC = () => {
    const record = useRecordContext<{
        id: number,
        document_ids: number[],
        user_id: number,
        endorsement_request_id: number | undefined,
        workflow_status: string,
    }>();
    const dataProvider = useDataProvider();
    const [paperOwners, setPaperOwners] = useState<OwnershipModel[]>([]);
    const [documents, setDocuments] = useState<any[] | undefined>(undefined);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(25);

    useEffect(() => {
        if (record?.user_id) {
            const fetchPaperOwners = async () => {
                const paperOwners = await dataProvider.getList('paper_owners', {
                    filter: {user_id: record.user_id}});
                setPaperOwners(paperOwners.data);
            };
            fetchPaperOwners();
        }
    }, [record, dataProvider]);

    useEffect(() => {
        if (paperOwners) {
            const fetchDocuments = async () => {
                const documentPromises = paperOwners.map((ownership) =>
                    dataProvider.getOne('documents', {id: ownership.document_id})
                );

                const documentResponses = await Promise.all(documentPromises);
                setDocuments(documentResponses.map(response => response.data));
            };

            fetchDocuments();
        }
    }, [paperOwners, dataProvider]);


    const handleChangePage = (event: unknown, newPage: number) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    if (documents === undefined) {
        return (<Typography>
            Other papers owned by the user - loading...
            </Typography>)
    }

    return (
        <>
            <Typography>
                Other papers owned by the user -{` ${documents.length} documents`}
            </Typography>
            <TablePagination
                rowsPerPageOptions={[10, 25, 100]}
                component="div"
                count={documents.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
            <Table>
                <TableHead>
                    <TableCell>
                        Owner
                    </TableCell>
                    <TableCell>Paper</TableCell>
                    <TableCell>Title</TableCell>
                    <TableCell>Authors</TableCell>
                    <TableCell>Date</TableCell>
                </TableHead>
                {documents.slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage).map((document, index) => (
                    <TableRow>
                        <TableCell>
                            {paperOwners[index].flag_author ? <YesIcon /> : null}
                        </TableCell>
                        <TableCell>
                            <ReferenceField source="id" reference="documents" record={document} link="show">
                                <TextField source="paper_id" />
                            </ReferenceField>
                        </TableCell>
                        <TableCell>
                            {document.title}
                        </TableCell>
                        <TableCell>
                            {document.authors}
                        </TableCell>
                        <TableCell>
                            {document.dated}
                        </TableCell>
                    </TableRow>
                ))}
            </Table>
        </>
    );
};


const RequestedPaperList: React.FC = () => {
    const record = useRecordContext<{
        id: number,
        document_ids: number[],
        user_id: number,
        endorsement_request_id: number | undefined,
        workflow_status: string,
    }>();
    const dataProvider = useDataProvider();
    const [documents, setDocuments] = useState<any[] | undefined>(undefined);
    const [paperOwners, setPaperOwners] = useState<any[] | undefined>(undefined);

    useEffect(() => {
        if (record?.document_ids) {
            const fetchDocuments = async () => {
                const documentPromises = record?.document_ids.map((doc_id) =>
                    dataProvider.getOne('documents', {id: doc_id})
                );

                const documentResponses = await Promise.all(documentPromises);
                setDocuments(documentResponses.map(response => response.data));
            };

            fetchDocuments();
        }
    }, [record, dataProvider]);

    useEffect(() => {
        if (documents && record) {
            const fetchOwnership = async () => {
                const ownershipPromises = documents.map(async (doc) => {
                    const fake_id = `user_${record.user_id}-doc_${doc.id}`;
                    try {
                        const response = await dataProvider.getOne('paper_owners', { id: fake_id });
                        return response.data;
                    } catch (error) {
                        return {
                            id: fake_id,
                            document_id: doc.document_id,
                            user_id: doc.user_id,
                            valid: false,
                            flag_author: false,
                            falg_auto: false
                        };
                    }
                });

                const ownershipResponses = await Promise.all(ownershipPromises);
                setPaperOwners(ownershipResponses);
            };

            fetchOwnership();
        }
    }, [record, documents, dataProvider]);

    if (paperOwners === undefined || documents === undefined) {
        return (<Typography>
            Requested papers - loading...
        </Typography>)
    }

    return (
        <>
            <Typography>
                Requested papers
            </Typography>
            <Table>
                <TableHead>
                    <TableCell>
                    <Tooltip title={"If this is on, the user is already a owner"}><span>Owner</span></Tooltip>
                    </TableCell>
                    <TableCell>Paper</TableCell>
                    <TableCell>Title</TableCell>
                    <TableCell>Authors</TableCell>
                    <TableCell>Date</TableCell>
                </TableHead>
                {documents.map((document, index) => (
                    <TableRow>
                        <TableCell>
                            <RecordContextProvider key={document.id} value={paperOwners[index]} >
                                <BooleanInput name={`flag_author_doc_${document.id}`} source="flag_author" label=""/>
                            </RecordContextProvider>
                        </TableCell>
                        <TableCell>
                            <ReferenceField source="id" reference="documents" record={document} link="show">
                                <TextField source="paper_id" />
                            </ReferenceField>
                        </TableCell>
                        <TableCell>
                            {document.title}
                        </TableCell>
                        <TableCell>
                            {document.authors}
                        </TableCell>
                        <TableCell>
                            {document.dated}
                        </TableCell>
                    </TableRow>
                ))}
            </Table>
        </>
    );
};


export const OwnershipRequestEdit = () => {
    const dataProvider = useDataProvider();

    return (
        <Edit title={<OwnershipRequestTitle />}>
            <SimpleForm>
                <RadioButtonGroupInput
                    source="workflow_status"
                    choices={[
                        { id: 'accepted', name: 'Accept' },
                        { id: 'rejected', name: 'Reject' },
                        { id: 'pending', name: 'Pending' },
                    ]}
                    label="Workflow Status"
                />
                <Card >
                    <CardContent>
                        <Table>
                            <TableHead>
                                <TableCell>User</TableCell>
                                <TableCell>Email</TableCell>
                                <TableCell>Info</TableCell>
                            </TableHead>
                            <TableRow>
                                <TableCell>
                                    <ReferenceField source="user_id" reference="users"
                                                    link={(record, reference) => `/${reference}/${record.id}`} >
                                        <TextField source={"last_name"} />
                                        {", "}
                                        <TextField source={"first_name"} />
                                    </ReferenceField>
                                </TableCell>
                                <TableCell>
                                    <ReferenceField source="user_id" reference="users">
                                        <EmailField source={"email"} />
                                    </ReferenceField>
                                </TableCell>
                                <TableCell>
                                    <ReferenceField source="id" reference="ownership_requests_audit" label={"Audit"}>
                                        {"Remote host: "}
                                        <TextField source={"remote_host"} defaultValue={"Unknown"}/>
                                        {"Date: "}
                                        <DateField source={"date"} />
                                    </ReferenceField>

                                </TableCell>
                            </TableRow>
                        </Table>
                        <RequestedPaperList />
                    </CardContent>
                </Card>
            </SimpleForm>
            <PaperOwnerList />
        </Edit>
    );
}

export const OwnershipRequestCreate = () => (
    <Create>
        <SimpleForm>
            <ReferenceInput source="ownershipRequestname" reference="ownershipRequests" />
            <TextInput source="first_name" />
            <TextInput source="last_name" />
            <TextInput source="email" />
        </SimpleForm>
    </Create>
);


export const OwnershipRequestShow = () => (
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
