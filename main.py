def main():
    state = new_state()
    scene = "camp"

    while True:
        if scene == "camp":
            scene = camp(state)
        elif scene == "ranger":
            scene = ranger(state)
        elif scene == "woods":
            scene = woods(state)
        elif scene == "tent":
            scene = tent(state)
        elif scene == "firepit":
            scene = firepit(state)
        elif scene == "end":
            ending(state)
            break
