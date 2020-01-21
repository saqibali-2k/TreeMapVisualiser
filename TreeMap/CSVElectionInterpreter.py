import pandas
from pandas import DataFrame
from os import listdir
from os.path import isfile, join
from typing import List
from DataTree import DataTree

"""Builder class for panda Ontario frames (elections).
"""


class CSVElectionInterpreter:
    election_data: DataFrame
    PARTIES: List[str]

    def __init__(self, path):
        csv_lst = [join('data', entry) for entry in listdir('data') if isfile(join('data', entry))]
        dataframes = []  # a list to hold all the individual pandas DataFrames
        for csv_file in csv_lst:
            df = pandas.read_csv(csv_file)
            dataframes.append(df)
        self.election_data = pandas.concat(dataframes, ignore_index=True)
        self._clean_data()
        self.PARTIES = ['Liberal', 'Conservative', 'Bloc Québécois', 'Green Party', 'NDP']

    def _clean_data(self):
        # unecessary information
        self.election_data = self.election_data.drop(['Electoral District Number/Numéro de circonscription',
                                                      'Polling Stations/Bureaux de scrutin',
                                                      'Population',
                                                      'Electors/Électeurs',
                                                      'Valid Ballots/Bulletins valides'],
                                                      axis=1)

        # Convert String data to numeric
        self.election_data['Total Ballots Cast/Total des bulletins déposés'] = pandas.to_numeric(
            self.election_data['Total Ballots Cast/Total des bulletins déposés'])

    def get_total_votes(self) -> int:
        return self.election_data['Candidate Poll Votes Count/Votes du candidat pour le bureau'].sum()

    def _get_party(self, dataframe_row) -> str:
        for party in self.PARTIES:
            if party in dataframe_row['Elected Candidate/Candidat élu']:
                return party
        return 'other'

    def get_dict(self) -> dict:
        curr_province = self.election_data['Province'].iloc[0]
        data = {'name': 'Canada', 'size': 0, 'category': '', 'subtrees': {}}
        province_data = data['subtrees']
        for index, row in self.election_data.iterrows():
            print(curr_province)
            curr_province = row['Province']
            district = row['Electoral District Name/Nom de circonscription']
            votes = row['Total Ballots Cast/Total des bulletins déposés']
            cat = self._get_party(row)
            if curr_province not in province_data:
                province_data[curr_province] = {}
                province_data[curr_province]['name'] = curr_province
                province_data[curr_province]['size'] = 0
                province_data[curr_province]['category'] = None
                province_data[curr_province]['subtrees'] = {}
            province_data[curr_province]['subtrees'][district] = {}
            sub_dict = province_data[curr_province]['subtrees'][district]
            sub_dict['name'] = district
            sub_dict['size'] = votes
            sub_dict['category'] = cat
            sub_dict['subtrees'] = {}
        return data









