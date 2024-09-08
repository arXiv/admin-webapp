import React, {useEffect, useState} from "react";
import { Link } from 'react-router-dom';
import {Card, CardContent, CardHeader, Grid, Button} from '@mui/material';
import {useDataProvider} from "react-admin";
import Typography from "@mui/material/Typography";
import {EndorsementRequestEdit} from "./endorsementRequests";


interface SummaryProps {
    resource: string;
    title: string;
    days: number;
}

const ResourceSummary: React.FC<SummaryProps> = ({ resource, title, days }) => {
    const [count, setCount] = useState<number | string>('Loading...');
    const dataProvider = useDataProvider();

    useEffect(() => {
        const fetchData = async () => {
            try {
                let dateRange: string = `last_${days}_days`;

                const response = await dataProvider.getList(resource, {
                    filter: { preset: dateRange, _start: null, _end: null },
                });
                setCount(response?.total || 0);
            } catch (error) {
                setCount('Error');
                console.error('Error fetching data', error);
            }
        };

        fetchData();
    }, [days, dataProvider]);

    return (
        <Grid container item xs={12}>
            <Grid item xs={3}>
                <Typography variant="subtitle1">{title}</Typography>
            </Grid>
            <Grid item xs={3}>
                <Typography variant="h6">{count}</Typography>
            </Grid>
        </Grid>
    );
};


export const Dashboard = () => {
    const dataProvider = useDataProvider();

    return (
        <Grid container>
            <Grid item xs={5}>
        <Card>
            <CardHeader title="Submission status" />
            <CardContent>
                <Grid container spacing={2}>
                    <Grid item xs={12}>
                        <Grid item container xs={12}>
                            <Typography variant="body1" color="textSecondary">Endorsement Request Summary</Typography>
                            <Grid item container xs={12}>
                                <ResourceSummary resource={"endorsement_requests"} days={1} title={"Today"} />
                                <ResourceSummary resource={"endorsement_requests"} days={7} title={"Last 7 days"} />
                                <ResourceSummary resource={"endorsement_requests"} days={60} title={"Last 60 days"} />
                                <ResourceSummary resource={"endorsement_requests"} days={365} title={"Last 365 days"} />
                            </Grid>
                        </Grid>

                        <Grid item container xs={12}>
                            <Typography variant="body1" color="textSecondary">Endorsement Summary</Typography>
                            <Grid item container xs={12}>
                                <ResourceSummary resource={"endorsements"} days={1} title={"Today"} />
                                <ResourceSummary resource={"endorsements"} days={7} title={"Last 7 days"} />
                                <ResourceSummary resource={"endorsements"} days={30} title={"Last 30 days"} />
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </CardContent>
        </Card>
        </Grid>
            <Grid item xs={5}>
                <Card>
                    <CardHeader title="Users" />
                    <CardContent>
                        <Grid container spacing={2}>
                            <Grid item xs={12}>
                                <Grid item container xs={12}>
                                    <Button component={Link} to={{ pathname: '/users', search: '?filter={"flag_edit_users":true}' }}>
                                        Administrators
                                    </Button>
                                    <Button component={Link} to={{ pathname: '/users', search: '?filter={"flag_is_mod":true}' }}>
                                        Moderators
                                    </Button>
                                    <Button component={Link} to={{ pathname: '/users', search: '?filter={"suspect":true}' }}>
                                        Suspect Users
                                    </Button>
                                </Grid>
                            </Grid>
                        </Grid>
                    </CardContent>
                </Card>
            </Grid>

        </Grid>
    );
}