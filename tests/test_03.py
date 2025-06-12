import pytest
from main import send_notification, send_dialog

history = []
scenario_name = "test_03"

def test_03():
    # Send information about the player character
    reply = send_notification("Player character is Yuv", history, scenario_name)
    assert "OK" in reply

    hero_description = """
    Introduction:
    Yuv is a young and relatively inexperienced hunter, introduced as someone still adapting to the harsh and disciplined life in the Hunter's Valley. Through his journey, he transforms from a naive youth into a braver and more aware individual.
    Development:
    Initially, Yuv appears passive and tired, overwhelmed by the journey and the demands placed on him. Despite his fatigue, he follows orders and sets out into the forest. His internal monologue reveals frustration and insecurity, making him relatable as someone still learning his place in the world. However, his curiosity and sense of duty drive him forward—even when he stumbles upon disturbing signs like the ruined logging camp or Alan’s corpse. Faced with fear, Yuv chooses to act—running to warn others, returning to help Terry, and attempting to stay alert during his watch. His fear is real, but he does not let it paralyze him completely.
    Conclusion:
    Yuv represents the coming-of-age arc in the story. He is not yet a hero, but he shows the potential to become one. His reactions to danger, though imperfect, are driven by courage and empathy. His journey is about learning to survive—and to care—in a world full of silent threats.
    """

    reply = send_notification(hero_description, history, scenario_name)
    assert "OK" in reply

    # Send information about the NPCs ###############################################################
    npc_description = """
    Introduction:
    Orr is one of the senior hunters in the group residing in the secluded Hunter's Valley. As a veteran, he carries the weight of responsibility and experience, which shapes his commanding and pragmatic personality.
    Development:
    Orr is portrayed as a no-nonsense, disciplined individual who values efficiency over comfort. He wakes Yuv up with immediate orders, assigning him tasks without delay or empathy for his fatigue. His curt, practical demeanor demonstrates his military-like mindset. Despite his gruffness, Orr is deeply responsible and protective. When danger arises, he acts swiftly—grabbing his bow and saving Yuv from a deadly wolf without hesitation. His leadership is calm and decisive, based on experience rather than emotion.
    Conclusion:
    Orr may appear harsh and distant, but his actions prove that he cares for the safety and survival of his team. He is the embodiment of a seasoned leader who has seen much and lets his actions speak louder than words.
    """

    reply = send_notification(npc_description, history, scenario_name)
    assert "OK" in reply
    ################################################################################################

    npc_description = """
    Introduction:
    Artur, another senior member of the hunting party, serves as a bridge between the harsh reality of the wilderness and the younger members' inexperience. His demeanor is warmer and more approachable than Orr's.
    Development:
    From the beginning, Artur shows empathy toward Yuv, giving him helpful advice rather than just commands. He seems to understand the challenges faced by the younger hunters and supports them subtly. In moments of crisis, however, Artur shows that he is no less courageous than Orr—quickly reacting to Yuv's report of Alan’s death, acknowledging the return of wolves, and helping save Terry. Artur is thoughtful and emotionally aware, evident in his concern for Terry’s family and his shock when learning about Alan’s fate.
    Conclusion:
    Artur balances strength and compassion. He brings a human element to the group’s hardened survivalism, making him a vital presence in both everyday life and moments of crisis."
    """

    reply = send_notification(npc_description, history, scenario_name)
    assert "OK" in reply
    ################################################################################################

    npc_description = """
    Introduction:
    Alan is a young hunter and one of Yuv's companions in the story \"Hunter's Valley\". Though his role in the narrative is relatively brief, his presence—and especially his tragic fate—have a profound impact on the tone and development of the plot.
    Development:
    At the beginning of the story, Alan is already gone from the shared tent he occupies with Yuv, indicating that he is an early riser and likely dedicated to his tasks. It is implied that he and Terry went out to collect wood, showing initiative and responsibility. However, Alan’s character is revealed more through the consequences of his actions than through direct interaction. When Yuv finds Alan’s lifeless, mutilated body in the ruins of the old logging camp, it serves as a turning point in the story—shifting the tone from an ordinary hunting trip to a tale of real danger and suspense.
    Although we see little of Alan’s personality directly, the emotional reaction of Yuv, as well as the urgency in the response from Orr and Artur, suggest that Alan was a respected and valued member of the group. His death is not treated lightly, and his loss creates a sense of vulnerability and fear among the remaining characters.
    Conclusion:
    Alan represents the fragility of life in the wilderness and serves as a narrative catalyst that transforms a seemingly mundane setting into a place of lurking danger. Even without many spoken lines or actions, his death leaves a significant emotional and psychological impact on the group, particularly on Yuv."
    """

    reply = send_notification(npc_description, history, scenario_name)
    assert "OK" in reply
    ################################################################################################

    # Test ###############################################################
    reply = send_notification("Started dialog with Artur", history, scenario_name)
    assert "OK" in reply

    dialog = """
dialogs:
  - dialog: 0
    talk:
    - who: NPC
      text: I hear Orr sent another youngster to look for black chanterelles?
    - who: HERO
      text: Yes, he said it's good practice to start with.
    - who: NPC
      text: Ha! He does that to every newcomer. I think he enjoys watching you wander through the woods.
    - who: NPC
      text: But since you got stuck with the task, head south, toward the old lumberjack camp.
    - who: NPC
      text: Whole patches of chanterelles grow there — if you know where to look.
    - who: NPC
      text: Alan and Terry also went there this morning. Maybe you'll catch up with them.
    - who: NPC
      text: Just be careful — the forest can be tricky this time of day. Especially when you're alone.
  - dialog: 1
    choice:
    - text: Thanks for the tip, I’m heading out right away.
      action:
      - next: 2
  - dialog: 2
    talk:
    - who: HERO
      text: Thanks for the tip, I’m heading out right away.
    - who: NPC
      text: Good luck, kid. And remember — not everything that looks like a chanterelle is edible!

    """

    send_dialog(dialog, history, scenario_name)

    reply = send_notification("Added water of 1 to a player's inventory", history, scenario_name)
    assert "OK" in reply

    reply = send_notification("Started dialog with Orr", history, scenario_name)
    assert "OK" in reply

    dialog = """
dialogs:
  - dialog: 0
    talk:
    - who: NPC
      text: Oh! I see you've finally woken up!
    - who: NPC
      text: You slept so long, I thought some forest spirit had dragged you into the cabin.
    - who: HERO
      text: A long journey takes its toll. I didn't expect to be this tired.
    - who: NPC
      text: A long journey? I thought you were here to hunt, not for a vacation.
    - who: NPC
      text: Anyway, do you have the energy now? If so, we could use some firewood.
    - who: NPC
      text: The fire won’t keep itself going, and Alan and Terry still haven’t returned.
    - who: NPC
      text: And since you’ll be out in the forest... bring me some black chanterelles.
    - who: NPC
      text: Dinner will taste better that way.
  - dialog: 1
    choice:
    - text: Sure, I’ll head into the forest right away.
      action:
      - next: 2
    - text: Maybe something to drink first?
      action:
      - next: 3
    - text: Where should I look?
      action:
      - next: 4
  - dialog: 2
    talk:
    - who: NPC
      text: Go on, go on.
  - dialog: 3
    talk:
    - who: NPC
      text: Lucky for you, we already fetched water from the stream.
    - who: NPC
      text: The water barrel is next to Arthur's cabin.
  - dialog: 4
    talk:
    - who: NPC
      text: Head toward the old lumberjack camp — there's always something there.
    """

    send_dialog(dialog, history, scenario_name)

    for i in range(10):
        reply = send_notification("Added black chanterelles of 1 to a player's inventory", history, scenario_name)
        assert "OK" in reply

    reply = send_notification("Hero finds Alan dead", history, scenario_name)
    assert "OK" in reply

    dialog = """
dialogs:
  - dialog: 0
    talk:
    - who: HERO
      text: No... this can't be...
    """
    send_dialog(dialog, history, scenario_name)
