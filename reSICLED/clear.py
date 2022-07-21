import brightway2 as bw

#print(bw.projects)
a =input("which project do you want to clear ?")
bw.projects.set_current(a)
for db in bw.databases:
    bw.Database(db).delete()