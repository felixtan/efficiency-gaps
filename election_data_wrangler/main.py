#!usr/bin/env python

import os
import sys
import config
import operator
import election_results.utils as utils
from processor.house_election_results import HouseElectionsProcessor


def print_states_and_properties(results):
    for state in results.state_results:
        state_results = results.state_results[state]
        print('\nstate: {}'.format(state))
        for field in state_results.__dict__:
            print('{}: {}'.format(field, state_results.__dict__[field]))


def get_states_and_eff_gaps(results):
    return [
        (
            state_results.state,
            state_results.efficiency_gap
        )
        for state_results in results.state_results.values()
    ]


def get_number_of_dists(state_results):
    return len(
        state_results.districts_won_rep +
        state_results.districts_won_dem
    )


def get_states_and_number_of_districts(results):
    state_results_dict = results.state_results
    return [
        (
            sr.state,
            get_number_of_dists(sr)
        )
        for sr in state_results_dict.values()
    ]


def print_states_by_eff_gap(results):
    state_gap_tuples = get_states_and_eff_gaps(results)

    sorted_tuples = sorted(
        state_gap_tuples,
        key=operator.itemgetter(1),
        reverse=True
    )

    for i, t in enumerate(sorted_tuples):
        print('{}: {}'.format(i, t))


def print_states_by_eff_gap_magnitude(results):
    state_gap_tuples = get_states_and_eff_gaps(results)

    sorted_tuples = sorted(
        state_gap_tuples,
        key=lambda t: abs(t[1]),
        reverse=True
    )

    print('Magnitude of efficiency gap per state')
    for i, t in enumerate(sorted_tuples):
        print('{}: {}'.format(i, t))


def print_states_by_number_of_districts(results):
    tuples = get_states_and_number_of_districts(results)

    sorted_tuples = sorted(
        tuples,
        key=operator.itemgetter(1),
        reverse=True
    )

    print('Number of districts per state')
    for i, t in enumerate(sorted_tuples):
        print('{}: {}'.format(i, t))


def print_states_by_magnitude_of_seat_advantage(results):
    state_results_dict = results.state_results

    tuples = [
        (
            sr.state,
            round(sr.efficiency_gap * get_number_of_dists(sr), 2)
        )
        for sr in state_results_dict.values()
    ]

    sorted_tuples = sorted(
        tuples,
        key=lambda t: abs(t[1]),
        reverse=True
    )

    print('Magnitude of seat advantage per state')
    for i, t in enumerate(sorted_tuples):
        print('{}: {}'.format(i, t))

    gross_net_seat_advantage = sum([s[1] for s in tuples])
    print('Gross net national seat advantage: {}'.format(
        gross_net_seat_advantage
    ))

    # Because there are no fractions of seats
    real_net_seat_advantage = sum([int(s[1]) for s in tuples])
    print('Real net national seat advantage: {}'.format(
        real_net_seat_advantage
    ))


#################
# DB operations #
#################
TABLES = [
    "states",
    "elections",
    "state_election_results",
    "district_election_results"
]

def get_number_of_rows(cursor, table_name):
    cursor.execute("select count(*) from {};".format(table_name))
    return cursor.fetchone()[0]


# The recommended way in SQL and psycopg2 for passing
# query params into statements doesn't work for table
# names so do this instead.
def check_table_exists(table_name):
    if isinstance(table_name, str):
        return "select id from {} limit 1;".format(table_name)
    else:
        raise TypeError("{} is not a string.")


def table_is_empty(cursor, table_name):
    try:
        cursor.execute(check_table_exists(table_name))
        return get_number_of_rows(cursor, table_name) == 0
    except (psycopg2.Error, TypeError) as e:
        print("Error: {}".format(e))

        # Assume that the psycopg2.Error is due to table not existing
        return isinstance(e, psycopg2.Error)


def create_tables(db_connection):
    cursor = db_connection.cursor()

    try:
        ###################
        # DROP ALL TABLES #
        ###################
        if opts["drop_tables"]:
            try:
                # TODO: generate this statement using the global const TABLES
                drop_all_tables = """
                    drop table district_election_results cascade;
                    drop table state_election_results cascade;
                    drop table elections cascade;
                    drop table states cascade;
                """

                print("WARNING: Dropping all tables from the db...")
                # TODO: Pose y/n prompt

                cursor.execute(drop_all_tables)
                print("Recreating tables...")

            except psycopg2.Error as e:
                raise e

        #######################
        # Create States table #
        #######################
        try:
            create_states_table = """
                create table if not exists states (
                    state_id    serial    primary key    not null,
                    iso_a2      char(2)                  not null,
                    name        char(14)                 not null
                );
            """
            cursor.execute(create_states_table)
            print('Created states table...')

        except psycopg2.Error as e:
            raise e

        ##########################
        # Create Districts table #
        ##########################
        # if table_is_empty(cursor, 'districts'):
        #     try:
        #         create_districts_table = """
        #             create table if not exists districts (
        #                 id          serial      primary key                    not null,
        #                 state_id    smallint    references states(state_id)    not null,
        #                 number      smallint                                   not null
        #             );
        #         """
        #         cursor.execute(create_districts_table)
        #         print('Created districts table...')
        #
        #     except psycopg2.Error as e:
        #         raise e
        #
        # else:
        #     print('Table districts exists.')

        ##########################
        # Create Elections table #
        ##########################
        try:
            create_elections_table = """
                create table if not exists elections (
                    election_id    serial    primary key    not null,
                    state          char(2)                  not null,
                    year           smallint                 not null
                );
            """
            cursor.execute(create_elections_table)
            print('Created elections table...')

        except psycopg2.Error as e:
            raise e

        #####################################
        # Create StateElectionResults table #
        #####################################
        try:
            create_state_election_results_table = """
                create table if not exists state_election_results (
                    election_id         smallint    primary key    references elections(election_id)    not null,
                    votes_dem           int                                                             not null,
                    votes_rep           int                                                             not null,
                    votes_other         int                                                             not null,
                    votes_total         int                                                             not null,
                    votes_wasted_dem    int                                                             not null,
                    votes_wasted_rep    int                                                             not null,
                    votes_wasted_net    int                                                             not null,
                    efficiency_gap      numeric(3,3)                                                    not null
                );
            """
            cursor.execute(create_state_election_results_table)
            print('Created state_election_results table...')

        except psycopg2.Error as e:
            raise e

        ########################################
        # Create DistrictElectionResults table #
        ########################################
        try:
            create_district_election_results = """
                 create table if not exists district_election_results (
                     district_election_results_id    serial      primary key                          not null,
                     election_id                     smallint    references elections(election_id)    not null,
                     number                          smallint                                         not null,
                     votes_dem                       int                                              not null,
                     votes_rep                       int                                              not null,
                     votes_other                     int                                              not null,
                     votes_total                     int                                              not null,
                     votes_wasted_dem                int                                              not null,
                     votes_wasted_rep                int                                              not null,
                     votes_wasted_net                int                                              not null
                 );
            """
            cursor.execute(create_district_election_results)
            print('Created district_election_results table...')

        except psycopg2.Error as e:
            raise e

        #############################
        # Populate the States table #
        #############################
        from fixtures.states import states as states_json

        states = [
            (iso_a2, states_json[iso_a2]) for iso_a2 in states_json
        ]

        try:
            insert_state = """
                insert into states (iso_a2, name)
                select %s, %s
                where not exists (select state_id from states where iso_a2 = %s)
                returning state_id;
            """

            for state in states:
                iso_a2 = state[0]
                name = state[1]
                cursor.execute(insert_state, [iso_a2, name, iso_a2])

        except psycopg2.Error as e:
            raise e

        # Persist the changes to the db
        db_connection.commit()

    except psycopg2.Error as e:
        print('Error: {}'.format(e))


def populate_tables(db_connection, national_election_results):
    cursor = db_connection.cursor()
    state_results = national_election_results.state_results

    rows_in_elections_before = get_number_of_rows(cursor, 'elections')
    rows_in_state_election_results_before = get_number_of_rows(cursor, 'state_election_results')
    rows_in_district_election_results_before = get_number_of_rows(cursor, 'district_election_results')

    for state in state_results:

        sr = state_results[state]

        # Get the state_id
        cursor.execute("""
            select state_id from states where iso_a2 = %s;
        """, (state,))
        state_id = cursor.fetchone()[0]

        # Insert into elections table
        cursor.execute("""
            insert into elections (state, year)
            select %s, %s
            where not exists (select election_id from elections where state = %s and year = %s)
            returning election_id;
        """, [state, int(sr.year), state, int(sr.year)])
        election_id = cursor.fetchone()[0]
        print('Created row in election for {} {}'.format(state, sr.year))

        # Insert into state_election_results table
        cursor.execute("""
            insert into state_election_results (election_id, votes_dem, votes_rep, votes_other, votes_total, votes_wasted_dem, votes_wasted_rep, votes_wasted_net, efficiency_gap)
            select %s, %s, %s, %s, %s, %s, %s, %s, %s
            where not exists (select * from state_election_results where election_id = %s);
        """, [election_id, sr.votes_total_dem, sr.votes_total_rep, sr.votes_total_other, sr.votes_total, sr.votes_wasted_total_dem, sr.votes_wasted_total_rep, sr.votes_wasted_net, sr.efficiency_gap, election_id])
        print('Created row in state_election_results for {} {}'.format(state, sr.year))

        # Insert into district_election_results table
        district_results = sr.districts_won_dem + sr.districts_won_rep
        for dr in district_results:
            number = int(dr.district)
            cursor.execute("""
                insert into district_election_results (election_id, number, votes_dem, votes_rep, votes_other, votes_total, votes_wasted_dem, votes_wasted_rep, votes_wasted_net)
                select %s, %s, %s, %s, %s, %s, %s, %s, %s
                where not exists (select * from district_election_results where election_id = %s and number = %s);
            """, [election_id, number, dr.votes_dem, dr.votes_rep, dr.votes_other, dr.votes_total, dr.votes_wasted_dem, dr.votes_wasted_rep, dr.votes_wasted_net, election_id, number])
            print('Created row in district_election_results for district {} {} {}'.format(dr.district, state, sr.year))

    db_connection.commit()

    # Summary
    print("{} rows inserted into elections table.".format(
        get_number_of_rows(cursor, 'elections') - rows_in_elections_before
    ))

    print("{} rows inserted into state_election_results table.".format(
        get_number_of_rows(cursor, 'state_election_results') - rows_in_state_election_results_before
    ))

    print("{} rows inserted into district_election_results table.".format(
        get_number_of_rows(cursor, 'district_election_results') - rows_in_district_election_results_before
    ))


def tables_exist(db_connection):
    try:
        cursor = db_connection.cursor()

        for t in TABLES:
            cursor.execute(check_table_exists(t))

    except (psycopg2.Error, TypeError) as e:
        print("Error: {}".format(e))
        return False

    return True


if __name__ == "__main__":
    election_year = sys.argv[1]
    flags = sys.argv[2:]

    # Options
    opts = {
        # For HouseElectionsProcessor
        "only_check_for_unhandled_elections": False,
        "print_modifications": False,
        "verbose_read": False,          # Print rows as they're read

        # For this script
        "create_tables": False,
        "quiet_mode": False,
        "drop_tables": False
    }

    for flag in flags:
        if flag == '--check-only' or flag == '-c':
            opts["only_check_for_unhandled_elections"] = True
        elif flag == '--print-mods' or flag == '-p':
            opts["print_modifications"] = True
        elif flag == '--create-tables':
            opts["create_tables"] = True
        elif flag == '--quiet_mode' or flag == '-q':
            opts["quiet_mode"] = True
        elif flag == '--verbose-read' or flag == '-v':
            opts["verbose_read"] = True
        elif flag == '--drop-tables':
            opts["drop_tables"] = True
        else:
            raise NameError('Unsupported flag {}'.format(flag))

    filename = election_year if election_year.endswith('.csv') \
        else election_year + '.csv'

    filepath = os.path.join(
        config.PATH_TO_HOUSE_ELECTION_RESULTS_DATA,
        filename
    )

    processor = HouseElectionsProcessor(
        year=election_year,

        # Options
        only_check_for_unhandled_elections=opts["only_check_for_unhandled_elections"],
        print_modifications=opts["print_modifications"],
        verbose_read=opts["verbose_read"]
    )

    try:
        results = processor.read_and_process_election_results(filepath)

        if not opts["quiet_mode"]:
            print_states_by_eff_gap_magnitude(results)
            print_states_by_magnitude_of_seat_advantage(results)

        try:
            import psycopg2

            conn = psycopg2.connect(
                dbname=config.DB_NAME_DEV,
                host=config.DB_HOST_DEV,
                user=config.DB_USER_DEV,
                password=config.DB_PASSWORD_DEV
            )

            create_tables(conn)
            populate_tables(conn, results)

        except psycopg2.Error as e:
            raise e

    except Exception as e:
        raise e
