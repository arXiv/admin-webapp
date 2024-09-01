import {useMediaQuery, ToggleButton, ToggleButtonGroup, Grid, Table, TableRow, TableCell} from '@mui/material';
import {
    List,
    SimpleList,
    Datagrid,
    TextField,
    EmailField,
    BooleanField,
    SortPayload,
    useRecordContext,
    Edit,
    SimpleForm, TextInput, ReferenceInput, Create, Filter, BooleanInput, DateField, ReferenceField, SelectInput
} from 'react-admin';

import DoDisturbOnIcon from '@mui/icons-material/DoDisturbOn';
import React, {useState} from "react";

const UserFilter = (props: any) => (
    <Filter {...props}>
        <BooleanInput label="Admin" source="flag_edit_users" />
        <BooleanInput label="Mod" source="flag_is_mod" />
        <BooleanInput label="Email verified" source="flag_email_verified" defaultValue={true} />
        <TextInput label="Search by Email" source="email" alwaysOn />
        <TextInput label="Search by First name" source="first_name"/>
        <TextInput label="Search by Last Name" source="last_name"/>
        <BooleanInput label="Email bouncing" source="email_bouncing" defaultValue={false} />
        <BooleanInput label="Suspect" source="suspect" defaultValue={true} />
    </Filter>
);

export default UserFilter;

interface VisibleColumns {
    email: boolean,
    joinedDate:boolean,
    mod: boolean,
}

export const UserList = () => {
    const sorter: SortPayload = {field: 'user_id', order: 'ASC'};
    const isSmall = useMediaQuery<any>(theme => theme.breakpoints.down('sm'));
    const [visibleColumns, setVisibleColumns] = useState<VisibleColumns>(
        {
            email: false,
            joinedDate: false,
            mod: false,
        }
    );
    const handleToggle = (event: React.MouseEvent<HTMLElement>) => {
        const column = event.currentTarget.getAttribute('value');
        if (column) {
            const isSelected = event.currentTarget.getAttribute('aria-pressed') === 'true';
            setVisibleColumns((prevState) => ({
                ...prevState,
                [column]: !isSelected,
            }));
        }
    };

    return (
        <div>
            <ToggleButtonGroup
                aria-label="Column visibility"
                sx={{ marginBottom: '1em' }}
            >
                <ToggleButton
                    value={"email"}
                    selected={visibleColumns.email}
                    onClick={handleToggle}
                    aria-label="Show Email"
                >
                    Email
                </ToggleButton>
                <ToggleButton
                    value={"joinedDate"}
                    onClick={handleToggle}
                    selected={visibleColumns.joinedDate}
                    aria-label="Show Joined Date"
                >
                    Joined Date
                </ToggleButton>
            </ToggleButtonGroup>

                <List filters={<UserFilter/>}>
                {isSmall ? (
                    <SimpleList
                        primaryText={record => record.name}
                        secondaryText={record => record.username}
                        tertiaryText={record => record.email}
                    />
                ) : (

                    <Datagrid rowClick="show" sort={sorter}>
                        <TextField source="last_name"/>
                        <TextField source="first_name"/>
                        <TextField source="suffix_name" label={"S"}/>
                        <TextField source="username" label={"Login name"}/>

                        <EmailField source="email"/>
                        {
                            visibleColumns.joinedDate ? <DateField source="joined_date"/> : null
                        }
                        <BooleanField source="flag_edit_users" label={"Admin"} FalseIcon={null}/>
                        <BooleanField source="flag_is_mod" label={"Mod"} FalseIcon={null}/>
                        <BooleanField source="flag_banned" label={"Banned"} FalseIcon={null}
                                      TrueIcon={DoDisturbOnIcon}/>
                        <BooleanField source="flag_suspect" label={"Suspect"} FalseIcon={null}
                                      TrueIcon={DoDisturbOnIcon}/>
                        <ReferenceField source="moderator_id" reference="moderators"
                                        link={(record, reference) => `/${reference}/${record.moderator_id}`} >
                            <TextField source={"archive"} />
                            {"/"}
                            <TextField source={"subject_class"} />
                        </ReferenceField>

                    </Datagrid>
                )}
            </List>
        </div>
    );
};

const UserTitle = () => {
    const record = useRecordContext();
    return <span>User {record ? `"${record.last_name}, ${record.first_name}" - ${record.email}` : ''}</span>;
};

const policyClassChoices = [
    { id: 0, name: 'Owner' },
    { id: 1, name: 'Admin' },
    { id: 2, name: 'Public user' },
    { id: 3, name: 'Legacy user' },
];


export const UserEdit = () => (
    <Edit title={<UserTitle />}>
        <SimpleForm>
            <Grid container>
                <Grid item xs={6}>
                    <Table>
                        <TableRow>
                            <TableCell>
                                email
                            </TableCell>
                            <TableCell>
                                <TextInput source="email" />
                                <BooleanInput source="flag_email_verified" label={"Email verified"} />
                                <BooleanInput source="email_bouncing" label={"Email bouncing"} />
                            </TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>
                                name
                            </TableCell>
                            <TableCell>
                                <TextInput source="first_name" />
                                <TextInput source="last_name" />
                            </TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>
                                User name
                            </TableCell>
                            <TableCell>
                                <TextField source="username" />
                            </TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>
                                policy class
                            </TableCell>
                            <TableCell>
                                <SelectInput source="policy_class" choices={policyClassChoices} />
                                <BooleanInput source="flag_edit_users" label={"Admin"}/>
                                <BooleanInput source="flad_banned" label={"Banned"}/>
                            </TableCell>
                        </TableRow>
                    </Table>
                </Grid>

                <Grid item xs={6}>
                    <Table>
                        <TableRow>
                            <TableCell>
                                User ID
                            </TableCell>
                            <TableCell>
                                <TextField source="id" />
                            </TableCell>
                        </TableRow>
                        <TableRow>
                            <TableCell>
                                Last login
                            </TableCell>
                            <TableCell>
                                <TextField source="id" />
                            </TableCell>
                        </TableRow>
                    </Table>
                </Grid>
            </Grid>
        </SimpleForm>
    </Edit>
);

export const UserCreate = () => (
    <Create>
        <SimpleForm>
            <ReferenceInput source="username" reference="users" />
            <TextInput source="first_name" />
            <TextInput source="last_name" />
            <TextInput source="email" />
            <BooleanInput source="flag_email_verified" label={"Email verified"} />
            <BooleanInput source="flag_edit_users" label={"Admin"}/>
            <BooleanInput source="email_bouncing" label={"Email bouncing"} />
            <BooleanInput source="flad_banned" label={"Banned"}/>
        </SimpleForm>
    </Create>
);


