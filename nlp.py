from globals import *
from scene import *
import google.generativeai as genai
import os

def event_log_to_text(event_log):
    text = ""
    for e in event_log:
        
        text += f"{round(e.t, 2)}s - "
        if isinstance(e, DeathEvent):
            text += f"Player {e.fighter_id} (from team {e.team_id}) lost!"
            if e.team_lost:
                text += f" This means team {e.team_id} is out of the competition!"
            text += "\n"
        elif isinstance(e, ClashEvent):
            high_speed = 13
            high_rot_speed = 20

            speed_cue = ""
            speed1 = math.sqrt(e.fighter1_v.x**2 + e.fighter1_v.y**2)
            speed2 = math.sqrt(e.fighter2_v.x**2 + e.fighter2_v.y**2)
            rot_speed1 = math.fabs(e.fighter1_w)
            rot_speed2 = math.fabs(e.fighter2_w)
            if speed1 > high_speed or speed2 > high_speed:
                speed_cue = " at high speed"
            elif rot_speed1 > high_rot_speed or rot_speed2 > high_rot_speed:
                speed_cue = " rotating fast"
            
            text += f"Players {e.fighter1_id} (from team {e.fighter1_team_id}) and {e.fighter2_id} (from team {e.fighter2_team_id}) collided{speed_cue}."
            text += "\n"
        elif isinstance(e, EndEvent):
            text += "The game ended! "
            if e.was_win:
                text += f"Team {e.winner_team_id} won!"
            else:
                text += "And it was a draw!"
            text += "\n"
            break
        elif isinstance(e, ShrinkingStartsEvent):
            text += "Now the field starts shrinking!\n"
    return text

def get_gpt_narration(event_text):
    prompt_text = """
You are a sports commentator. The sport you are going to comment doesn't really exist, but pretend you saw a game of it in real life. The description is the following: there is a circular field, and some teams of tiny robots; the goal is for the robots to push the robots from other teams out of the field, just colliding with each other. If the match takes too long, the field will start shrinking, and that will be reflected in the event log.

Now you are going to be given an event log of a match. It consists of a number of lines, each describing something that happened on the match. The lines are given in the order the events unfolded. For example, if players 1 from team 0 and player 2 from team 3 collided at second 5, a line will say "5.0s - Players 1 (from team 0) and 2 (from team 3) collided.". In collision, events the teams of every player are logged so that you have more context (to know, for example, when the collision was accidental, between two members of the same team, and not a direct attack), but you should not emphasize the teams on collision events.

Your task is to give comment on the match as if you were a sports commentator. The event log of the match is given now:
"""
    prompt_text += event_text
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt_text)
    return response.text