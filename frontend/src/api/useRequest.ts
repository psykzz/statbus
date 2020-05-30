import useSWR, { ConfigInterface, responseInterface } from 'swr';
import axios, { AxiosResponse, AxiosError, AxiosRequestConfig } from 'axios';

export type GetRequest = (AxiosRequestConfig | {}) & {
    url: string;
};

interface Return<Data, Error>
    extends Pick<responseInterface<AxiosResponse<Data>, AxiosError<Error>>, 'isValidating' | 'revalidate' | 'error'> {
    data: Data | undefined;
    response: AxiosResponse<Data> | undefined;
}

export interface Config<Data = unknown, Error = unknown>
    extends Omit<ConfigInterface<AxiosResponse<Data>, AxiosError<Error>>, 'initialData'> {
    initialData?: Data;
}
export function useRequest<Data = unknown, Error = unknown>(
    initialRequest: GetRequest,
    { initialData, ...config }: Config<Data, Error> = {},
): Return<Data, Error> {
    const { ...request } = initialRequest;
    const swrRequestKey = request && JSON.stringify(request);
    const { data: response, error, isValidating, revalidate } = useSWR<AxiosResponse<Data>, AxiosError<Error>>(
        swrRequestKey,
        () => axios(request || {}),
        {
            ...config,
            initialData: initialData && {
                status: 200,
                statusText: 'InitialData',
                config: request,
                headers: {},
                data: initialData,
            },
        },
    );

    return {
        data: response && response.data,
        response,
        error,
        isValidating,
        revalidate,
    };
}
