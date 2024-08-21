import { Admin, Resource, ShowGuesser } from 'react-admin';
import React, {useEffect} from 'react';

import UserIcon from '@mui/icons-material/Group';
import EmailIcon from '@mui/icons-material/EmailOutlined';
import EndorsedEcon from '@mui/icons-material/Verified';
import RequestIcon from '@mui/icons-material/MeetingRoom';
import DocumentIcon from '@mui/icons-material/Book';

import {TemplateCreate, TemplateList, TemplateEdit} from './templates';
import { UserList, UserEdit, UserCreate } from './users';
import {EndorsementRequestList, EndorsementRequestCreate, EndorsementRequestEdit, EndorsementRequestShow} from './endorsementRequests';
import { Dashboard } from './Dashboard';
import { authProvider } from './authProvider';
import adminApiDataProvider from './adminApiDataProvider';
import {EndorsementCreate, EndorsementEdit, EndorsementList} from "./endorsements";
import {DocumentCreate, DocumentEdit, DocumentList} from "./documents";

const dataProvider = new adminApiDataProvider('http://127.0.0.1:5000/api/v1');

const RedirectComponent: React.FC<{to: string}> = ({ to }) => {
    useEffect(() => {
        console.log("to -> " + to);
        window.location.href = to;
    }, [to]);

    return null;
};

const App = () => (
    <Admin
        authProvider={authProvider}
        dataProvider={dataProvider}
        dashboard={Dashboard}
        loginPage={(<RedirectComponent to={"http://127.0.0.1:5000/api/login?next=http://127.0.0.1:5000"}/>)}
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



    </Admin>
);

export default App;
