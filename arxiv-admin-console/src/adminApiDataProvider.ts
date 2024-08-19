
import {
    fetchUtils,
    DataProvider,
    GetListResult,
    GetListParams,
    RaRecord,
    GetManyParams,
    GetManyResult
} from 'react-admin';
import jsonServerProvider from 'ra-data-json-server';

class adminApiDataProvider implements DataProvider {
    private dataProvider: DataProvider;
    private api: string;
    constructor(api: string) {
        this.api = api;
        this.dataProvider = jsonServerProvider(api);
    }
    async getList<T extends RaRecord>(resource: string, params: GetListParams): Promise<GetListResult<T>> {

        if (resource === 'subject_class' && params.filter.archive) {
            const { archive } = params.filter;
            const url = `${this.api}/categories/${archive}/subject-class/`;
            console.log("subject_class API " +  url);
            try {
                const response = await fetchUtils.fetchJson(url);
                return {
                    data: response.json as T[],
                    total: response.json.length,
                };
            }
            catch (error) {
                return {
                    data: [] as T[],
                    total: 0,
                };
            }
        }
        else if (resource === 'endorsees') {
            console.log("endorsees -> users");
            return this.dataProvider.getList<T>("users", params);
        }

        return this.dataProvider.getList<T>(resource, params);
    }

    getOne: typeof this.dataProvider.getOne = (resource, params) => this.dataProvider.getOne(resource, params);

    async getMany<T extends RaRecord>(resource: string, params: GetManyParams): Promise<GetManyResult<T>> {
        if (resource === 'endorsees') {
            console.log("endorsees -> users");
            return this.dataProvider.getMany<T>("users", params);
        }
        return this.dataProvider.getMany<T>(resource, params);
    }

    getManyReference: typeof this.dataProvider.getManyReference = (resource, params) => this.dataProvider.getManyReference(resource, params);
    create: typeof this.dataProvider.create = (resource, params) => this.dataProvider.create(resource, params);
    update: typeof this.dataProvider.update = (resource, params) => this.dataProvider.update(resource, params);
    updateMany: typeof this.dataProvider.updateMany= (resource, params) => this.dataProvider.updateMany(resource, params);
    delete: typeof this.dataProvider.delete = (resource, params) => this.dataProvider.delete(resource, params);
    deleteMany: typeof this.dataProvider.deleteMany = (resource, params) => this.dataProvider.deleteMany(resource, params);
}

export default adminApiDataProvider;
