import { Admin, Resource, ShowGuesser } from 'react-admin';
import React, {useContext, useEffect, useState} from 'react';

import UserIcon from '@mui/icons-material/Group';
import EmailIcon from '@mui/icons-material/EmailOutlined';
import EndorsedEcon from '@mui/icons-material/Verified';
import RequestIcon from '@mui/icons-material/MeetingRoom';
import DocumentIcon from '@mui/icons-material/Book';
import CategoryIcon from '@mui/icons-material/List';
import ModeratorIcon from '@mui/icons-material/Policy';
import OwnershipRequestIcon from '@mui/icons-material/Star';

import {TemplateCreate, TemplateList, TemplateEdit} from './templates';
import { UserList, UserEdit, UserCreate } from './users';
import {EndorsementRequestList, EndorsementRequestCreate, EndorsementRequestEdit, EndorsementRequestShow} from './endorsementRequests';
import { Dashboard } from './Dashboard';
import {createAuthProvider} from './authProvider';
import adminApiDataProvider from './adminApiDataProvider';
import {EndorsementCreate, EndorsementEdit, EndorsementList} from "./endorsements";
import {DocumentCreate, DocumentEdit, DocumentList} from "./documents";
import {CategoryList, CategoryCreate, CategoryEdit} from "./categories";
import {ModeratorCreate, ModeratorEdit, ModeratorList} from "./moderators";
import {OwnershipRequestEdit, OwnershipRequestList} from "./ownershipRequests";
import {RuntimeContext, RuntimeContextProvider} from "./RuntimeContext";


const RedirectComponent: React.FC<{to: string}> = ({ to }) => {
    useEffect(() => {
        console.log("to -> " + to);
        window.location.href = to;
    }, [to]);

    return null;
};

const AdminConsole: React.FC = () => {
    const runtimeProps = useContext(RuntimeContext);
    const dataProvider = new adminApiDataProvider(runtimeProps.ADMIN_API_BACKEND_URL);
    const authProvider = createAuthProvider(runtimeProps);

    return (
    <Admin
        authProvider={authProvider}
        dataProvider={dataProvider}
        dashboard={Dashboard}

        loginPage={(<RedirectComponent to={`${runtimeProps.AAA_URL}/login?next=${runtimeProps.ADMIN_APP_ROOT}`}/>)}
    >
        <Resource
            name="users"
            list={UserList}
            show={ShowGuesser}
            icon={UserIcon}
            recordRepresentation="name"
            edit={UserEdit}
            create={UserCreate}
        />

        <Resource
            name="email_templates"
            list={TemplateList}
            show={ShowGuesser}
            icon={EmailIcon}
            recordRepresentation="short_name"
            edit={TemplateEdit}
            create={TemplateCreate}
        />

        <Resource
            name="endorsements"
            list={EndorsementList}
            show={ShowGuesser}
            icon={EndorsedEcon}
            recordRepresentation="name"
            edit={EndorsementEdit}
            create={EndorsementCreate}
        />

        <Resource
            name="endorsement_requests"
            list={EndorsementRequestList}
            show={EndorsementRequestShow}
            icon={RequestIcon}
            recordRepresentation="name"
            edit={EndorsementRequestEdit}
            create={EndorsementRequestCreate}
        />

        <Resource
            name="documents"
            list={DocumentList}
            show={ShowGuesser}
            icon={DocumentIcon}
            recordRepresentation="name"
            edit={DocumentEdit}
            create={DocumentCreate}
        />

        <Resource
            name="categories"
            list={CategoryList}
            show={ShowGuesser}
            icon={CategoryIcon}
            recordRepresentation="name"
            edit={CategoryEdit}
            create={CategoryCreate}
        />

        <Resource
            name="moderators"
            list={ModeratorList}
            show={ShowGuesser}
            icon={ModeratorIcon}
            recordRepresentation="archive"
            edit={ModeratorEdit}
            create={ModeratorCreate}
        />

        <Resource
            name="ownership_requests"
            list={OwnershipRequestList}
            edit={OwnershipRequestEdit}
            show={ShowGuesser}
            icon={OwnershipRequestIcon}
            recordRepresentation="user_id"
        />

        <Resource name="endorsement_requests_audit"/>
        <Resource name="ownership_requests_audit"/>
        <Resource name="paper_owners"/>
        <Resource name="demographics"/>

    </Admin>
    )
}

const App = () => {
    return (
        <RuntimeContextProvider>
            <AdminConsole />
        </RuntimeContextProvider>
    );
}

export default App;
