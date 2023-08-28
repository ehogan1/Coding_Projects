from checkers_bot import BotTest

smart_tot = 0
rand_tot = 0
for i in range(25):
    test = BotTest()
    smart, rand = test.run_test(100)
    smart_tot += smart
    rand_tot += rand
smart_final = smart_tot / 25
rand_final = rand_tot / 25
print(smart_final, rand_final)
