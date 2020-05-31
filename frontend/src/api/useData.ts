import { useRequest } from "./useRequest";

export const useSummary = () => {
    const { data: { rounds = [], polls = [], stats = {} } = {}, ...rest } = useRequest<any>({
        url: `/api/summary`,
    });

    return { rounds, polls, stats, ...rest };
};

export const useWinrates = () => {
    const { data: { winrates = {} } = {}, ...rest } = useRequest<any>({
        url: `/api/winrate`,
    });

    return { winrates, ...rest };
};

export const useRounds = ({ page, limit }: { page?: number, limit?: number }) => {
    const { data: { rounds = [] } = {}, ...rest } = useRequest<any>({
        url: `/api/rounds/${page ?? 1}?limit=${limit ?? 30}`,
    });

    return { rounds, ...rest };
};

export const useRound = (roundId: number) => {
    const { data: { round = {} } = {}, ...rest } = useRequest<any>({
        url: `/api/round/${roundId}`,
    });

    return { round, ...rest };
};

export const usePullRequest = () => {
    const { data = [], ...rest } = useRequest<any>({
        url: `https://api.github.com/repos/tgstation/TerraGov-Marine-Corps/pulls`,
    });
    const filteredData: any = {}
    data.forEach((pr: any) => (filteredData[pr.number] = pr));

    return { data: filteredData, ...rest };
}
