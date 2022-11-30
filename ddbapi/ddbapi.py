import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import typing
from typing import overload
import pandas as pd

'''
Karl Krägelin
2021
kraegelin@sub.uni-goettingen.de
'''

def zp_issues(**query) -> pd.DataFrame:
    """Call DDB API, return a Dataframe Object.

    Keyword arguments:

    - `language`
    - `place_of_distribution`
    - `publication_date`
    - `zdb_id`
    - `provider`
    - `paper_title`

    Keyword arguments can contain lists.

    """

    def setup_requests() -> requests.Session:
        """Sets up a requests session to automatically retry on errors

        cf. <https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/>

        Returns
        -------
        http : requests.Session
            A fully configured requests Session object
        """
        http = requests.Session()
        assert_status_hook = (
            lambda response, *args, **kwargs: response.raise_for_status()
        )
        http.hooks["response"] = [assert_status_hook]
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    http = setup_requests()

    API_URL = "https://api.deutsche-digitale-bibliothek.de/search/index/newspaper-issues/select"
    # Construct Parameters for HTTP Query

    params = dict()
    params["rows"] = 1000
    params["sort"] = "id ASC"

    q = ["type:issue"]
    allowed_kwargs = ['language', 'place_of_distribution', 'publication_date', 'zdb_id', 'provider', 'paper_title']
    querytuples = [(k, query[k]) for k in query]
    for field, value in querytuples:
        if field not in allowed_kwargs:
            raise Exception(f"{field} ist nicht erlaubt")
        if field == "publication_date":
            # publication_date before 1677
            try:
                if int(value[1:5:1]) <= 1677:
                    problematic_Timestamp = True
                else:
                    problematic_Timestamp = False
            except:
                pass
        else:
            problematic_Timestamp = False

        if isinstance(value, list):
            # parameter has multiple values
            subq = []
            for i in value:
                i = i.replace(" ", "\ ")
                subq.append(f"{field}:{i}")
            q.append("(" + " AND ".join(subq) + ")")
        else:
            # parameter has only one value, not a list
            if field != "issue":
                value = value.replace(" ", "\ ")
                q.append(f'{field}:"{value}"')

    params["q"] = " AND ".join(q)
    params["cursorMark"] = "*"
    # Gettin the data
    try:
        http.get(API_URL, params=params)
    except Exception as e:
        return e
    else:
        print(http.get(API_URL, params=params).request.url)
        docs = []
        if http.get(API_URL, params=params).json()["response"]["numFound"] >= 1000:
            # if we have to iterate over the responses
            numFound = http.get(API_URL, params=params).json()["response"]["numFound"]
            while True:
                apireturn = http.get(API_URL, params=params).json()
                cursormark = apireturn["nextCursorMark"]
                params["cursorMark"] = cursormark
                if len(apireturn["response"]["docs"]) != 0:
                    docs.extend(apireturn["response"]["docs"])
                    print(f"Getting {len(docs)} of {numFound}")
                else:
                    break
        else:
            # if the return fits on one page
            response = http.get(API_URL, params=params).json()["response"]["docs"]
            if len(response) != 0:
                docs.extend(http.get(API_URL, params=params).json()["response"]["docs"])
            else:
                pass
        # construct Dataframe from List of returned documents
        df = pd.DataFrame(docs)
        print(f"Got {len(df)} items.")
        if len(df) != 0:

            df.rename(columns = {'id':'ddb_item_id'}, inplace = True)

            if problematic_Timestamp == False:
                # If Timestamp ist after 1677, pandas can convert the column into a datetime object.
                # See https://pandas.pydata.org/docs/user_guide/timeseries.html#timestamp-limitations
                df["publication_date"] = pd.to_datetime(
                    df["publication_date"], format="%Y-%m-%dT%H:%M:%SZ"
                )
            else:
                # otherwise transform data to python datetime type
                import datetime as dt

                df["publication_date"] = df["publication_date"].apply(
                    lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
                    if type(x) == str
                    else pd.NaT
                )
        else:
            pass
        return df


def zp_pages(**query) -> pd.DataFrame:
    """Call DDB API, return a Dataframe Object.

    Keyword arguments:

    - 'plainpagefulltext`
    - `language`
    - `place_of_distribution`
    - `publication_date`
    - `zdb_id`
    - `provider`
    - `paper_title`

    Keyword arguments can contain lists.

    """

    def setup_requests() -> requests.Session:
        """Sets up a requests session to automatically retry on errors

        cf. <https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/>

        Returns
        -------
        http : requests.Session
            A fully configured requests Session object
        """
        http = requests.Session()
        assert_status_hook = (
            lambda response, *args, **kwargs: response.raise_for_status()
        )
        http.hooks["response"] = [assert_status_hook]
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
            backoff_factor=1,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        http.mount("https://", adapter)
        http.mount("http://", adapter)
        return http

    http = setup_requests()

    API_URL = "https://api.deutsche-digitale-bibliothek.de/search/index/newspaper-issues/select"
    # Construct Parameters for HTTP Query

    params = dict()
    params["rows"] = 1000
    params["sort"] = "id ASC"

    q = ["type:page"]
    allowed_kwargs = ['plainpagefulltext', 'language', 'place_of_distribution', 'publication_date', 'zdb_id', 'provider', 'paper_title']
    querytuples = [(k, query[k]) for k in query]
    for field, value in querytuples:
        if field not in allowed_kwargs:
            raise Exception(f"{field} ist nicht erlaubt")
        if field == "publication_date":
            # publication_date before 1677
            try:
                if int(value[1:5:1]) <= 1677:
                    problematic_Timestamp = True
                else:
                    problematic_Timestamp = False
            except:
                pass
        else:
            problematic_Timestamp = False

        if isinstance(value, list):
            # parameter has multiple values
            subq = []
            for i in value:
                i = i.replace(" ", "\ ")
                subq.append(f"{field}:{i}")
            q.append("(" + " AND ".join(subq) + ")")
        else:
            # parameter has only one value, not a list
            if field != "issue":
                value = value.replace(" ", "\ ")
                q.append(f'{field}:"{value}"')

    params["q"] = " AND ".join(q)
    params["cursorMark"] = "*"
    # Gettin the data
    try:
        http.get(API_URL, params=params)
    except Exception as e:
        return e
    else:
        print(http.get(API_URL, params=params).request.url)
        docs = []
        if http.get(API_URL, params=params).json()["response"]["numFound"] >= 1000:
            # if we have to iterate over the responses
            numFound = http.get(API_URL, params=params).json()["response"]["numFound"]
            while True:
                apireturn = http.get(API_URL, params=params).json()
                cursormark = apireturn["nextCursorMark"]
                params["cursorMark"] = cursormark
                if len(apireturn["response"]["docs"]) != 0:
                    docs.extend(apireturn["response"]["docs"])
                    print(f"Getting {len(docs)} of {numFound}")
                else:
                    break
        else:
            # if the return fits on one page
            response = http.get(API_URL, params=params).json()["response"]["docs"]
            if len(response) != 0:
                docs.extend(http.get(API_URL, params=params).json()["response"]["docs"])
            else:
                pass
        # construct Dataframe from List of returned documents
        df = pd.DataFrame(docs)
        print(f"Got {len(df)} items.")
        if len(df) != 0:
            df.rename(columns={'id': 'page_id'}, inplace=True)
            try:
                # try to extract DDB Item ID, needs pagename
                df["ddb_item_id"] = df.apply(
                    lambda row: row.id.replace("-" + row.pagename, ""), axis=1
                )
            except:
                pass

            if problematic_Timestamp == False:
                # If Timestamp ist after 1677, pandas can convert the column into a datetime object.
                # See https://pandas.pydata.org/docs/user_guide/timeseries.html#timestamp-limitations
                df["publication_date"] = pd.to_datetime(
                    df["publication_date"], format="%Y-%m-%dT%H:%M:%SZ"
                )
            else:
                # otherwise transform data to python datetime type
                import datetime as dt

                df["publication_date"] = df["publication_date"].apply(
                    lambda x: dt.datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
                    if type(x) == str
                    else pd.NaT
                )
        else:
            pass
        return df


def list_column(series: pd.Series) -> pd.Series:
    '''Convert a list-containing column to a 2D array thus allowing us to apply typical pandas functions again'''
    return pd.Series([x for _list in series for x in _list])


def filter(searchfor: typing.Union[str, list], searchin: str, inframe: pd.DataFrame) -> pd.DataFrame:
    '''
    Search for a string or a list of strings inside columns containing lists of Pandas DataFrames. Returns a new, filtered DataFrame.
    '''
    if isinstance(searchfor, list):
        msk = inframe[searchin].apply(lambda row: any(i for i in searchfor if i in row))
        return inframe[msk]
    else:
        mask = inframe[searchin].apply(lambda row: searchfor in row)
        return inframe[mask]
