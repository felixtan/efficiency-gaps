from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from .models import State, Election, StateElectionResult
import json

@require_http_methods(['GET'])
def gaps_vs_year_for_all_states(request):
    data = {}
    states = State.objects.all()

    for state in states:
        points = []
        state_matches = "elections.state='{}'".format(state.iso_a2)
        elections = Election.objects.extra(where=[state_matches])

        for election in elections:
            election_id_matches = "election_id='{}'".format(election.election_id)
            election_results = StateElectionResult.objects.extra(where=[election_id_matches])

            for result in election_results:
                points.append((election.year, result.efficiency_gap))
                data[state.iso_a2] = points

    return HttpResponse(json.dumps(data, cls=DjangoJSONEncoder, sort_keys=True))
