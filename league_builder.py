import csv

def get_player_data(players_file):
	players = []
	with open(players_file) as g:
		raw_data = csv.DictReader(g)
		for line in raw_data:
			players.append(line)
		return players

def sort_players(players):
	"""
	Sorts players into experienced_players and rookies
	returning them in a tuple
	"""

	experienced_players = []
	rookies = []
	for player in players:
		if player['Soccer Experience'] == "YES":
			experienced_players.append(player)
		else:
			rookies.append(player)
	return (experienced_players,rookies)

def assign_players_to_teams(teams, experts, rookies):
	"""
	Builds a dictionary of teams 
	"""
	num_teams = len(teams)
	assigned_players = []
	team_lists = {"Dragons":[], "Raptors":[], "Sharks":[]}


	for expert in experts:
		team_index = experts.index(expert) % num_teams
		expert['Team'] = teams[team_index]
		assigned_players.append(expert)

	for rookie in rookies:
		team_index = rookies.index(rookie) % num_teams
		rookie['Team'] = teams[team_index]
		assigned_players.append(rookie)

	for player in assigned_players:
		team_lists[player['Team']].append(player)
	print(team_lists["Dragons"])	
	return team_lists

def load_letter_template():
	"""
	loads the letter template into a string
	"""

	template_letter = ""
	with open("letter_template.txt") as f:
		for line in f:
			template_letter += line
	return template_letter

def generate_letters(team_lists):
	practice = {"Dragons":"March 17, 1pm", 
				"Sharks":"March 17, 3pm", 
				"Raptors":"March 18, 1pm"}

	template_letter = load_letter_template()
	
	for team in team_lists:
		for player in team_lists[team]:
			player_letter = template_letter
			player_letter = player_letter.replace("{Guardian}", player["Guardian Name(s)"])
			player_letter = player_letter.replace("{Name}", player["Name"])
			player_letter = player_letter.replace("{Team}", team)
			player_letter = player_letter.replace("{Practice}", practice[team])
			print(player_letter)
			player_letter_file = player["Name"] + ".txt"

			with open(player_letter_file,'w') as p:
				p.write(player_letter)

def main():
	teams = ["Dragons", "Sharks", "Raptors"]
	players = get_player_data("soccer_players.csv")
	sorted_players = sort_players(players)
	players_in_teams = assign_players_to_teams(teams, sorted_players[0], sorted_players[1])
	generate_letters(players_in_teams)

if __name__ == "__main__":
	main()
