import { useMediaQuery } from '@mui/material';
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
    SimpleForm, TextInput, ReferenceInput, Create, Filter, BooleanInput, DateField
} from 'react-admin';

import DoDisturbOnIcon from '@mui/icons-material/DoDisturbOn';

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

export const UserList = () => {
    const sorter: SortPayload = {field: 'user_id', order: 'ASC'};
    const isSmall = useMediaQuery<any>(theme => theme.breakpoints.down('sm'));
    return (
        <List filters={<UserFilter />}>
            {isSmall ? (
                <SimpleList
                    primaryText={record => record.name}
                    secondaryText={record => record.username}
                    tertiaryText={record => record.email}
                />
            ) : (
                <Datagrid rowClick="show" sort={sorter}>
                    <TextField source="last_name" />
                    <TextField source="first_name" />
                    <TextField source="suffix_name" label={"S"}/>
                    <TextField source="username" label={"Login name"}/>
                    <EmailField source="email" />
                    <DateField source="joined_date" />
                    <BooleanField source="flag_edit_users" label={"Admin"} FalseIcon={null} />
                    <BooleanField source="flag_is_mod" label={"Mod"} FalseIcon={null} />
                    <BooleanField source="flag_banned" label={"Banned"} FalseIcon={null} TrueIcon={DoDisturbOnIcon} />
                    <BooleanField source="flag_suspect" label={"Suspect"} FalseIcon={null} TrueIcon={DoDisturbOnIcon} />
                </Datagrid>
            )}
        </List>
    );
};


const UserTitle = () => {
    const record = useRecordContext();
    return <span>User {record ? `"${record.last_name}, ${record.first_name}" - ${record.email}` : ''}</span>;
};

export const UserEdit = () => (
    <Edit title={<UserTitle />}>
        <SimpleForm>
            <TextInput source="id" disabled />
            <TextInput source="first_name" />
            <TextInput source="last_name" />
            <TextInput source="email" />
            <BooleanInput source="flag_email_verified" label={"Email verified"} />
            <BooleanInput source="flag_edit_users" label={"Admin"}/>
            <BooleanInput source="email_bouncing" label={"Email bouncing"} />
            <BooleanInput source="flad_banned" label={"Banned"}/>
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


