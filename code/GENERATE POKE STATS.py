import random

endstats = open("STATS.txt", "w")
reference = open("PULLS.txt", "r", encoding = 'cp850')
stars = 3
starstats = {3: 50, 4: 125, 5: 200, 6: 300}

#HP         attack def speed
for i in reference.read().split("\n"):
    if i == "-STAR UP-":
        stars += 1
    elif len(i.split("[]")) < 4:
        print("skipped ", i)
    else:
        print(" ")
        total = starstats[stars]
        print(total)
        hp = random.randint(1, int(total/2))
        total -= hp
        print(total)
        attack = random.randint(1, total-10)
        total -= attack
        print(total)
        defence = random.randint(1, total-5)
        total -= defence
        print(total)
        speed = stars*100 + total 
        hp = stars*100 + hp
        attack = stars*100 + attack
        defence = stars*100 + defence
        endstats.write(i.split("[]")[0] + ";;" + str(hp) + ";;" + str(attack) + ";;" + str(defence) + ";;" + str(speed) + "\n")


endstats.close()
reference.close()
