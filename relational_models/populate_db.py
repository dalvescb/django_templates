from examples import models

def populate():
    # Populate ProgrammmingLanguage Table
    models.ProgrammingLanguage.objects.create(name="python",paradigm="IM",is_oo=True)
    models.ProgrammingLanguage.objects.create(name="haskell",paradigm="FR",is_oo=False)
    models.ProgrammingLanguage.objects.create(name="c",paradigm="IM",is_oo=False)
    models.ProgrammingLanguage.objects.create(name="c++",paradigm="IM",is_oo=True)

    # Populate TestModel Table
    models.TestModel.objects.create(name="TestField1")
    models.TestModel.objects.create(name="TestField2")

    # Populate Company Table
    superInc = models.Company(name="SuperAwesomeInc")
    superInc.save()
    dumbCo = models.Company(name="ReallyDumbCo")
    dumbCo.save()

    # Populate Employee Table
    models.Employee.objects.create(name="GoodEmployee1",company=superInc)
    models.Employee.objects.create(name="GoodEmployee2",company=superInc)
    models.Employee.objects.create(name="GoodEmployee3",company=superInc)
    models.Employee.objects.create(name="GoodEmployee4",company=superInc)

    models.Employee.objects.create(name="BadEmployee1",company=dumbCo)
    models.Employee.objects.create(name="BadEmployee2",company=dumbCo)
    models.Employee.objects.create(name="BadEmployee3",company=dumbCo)

    # Populate Class Table
    class1 = models.Class(name="CS 1XA3")
    class1.save()
    class2 = models.Class(name="CS 1MD3")
    class2.save()

    # Populate the Student Table
    stud1 = models.Student.objects.create(name="GoodStudent1")
    stud1.classes.add(class1)
    stud1.save()
    stud2 = models.Student.objects.create(name="GoodStudent2")
    stud2.classes.add(class1)
    stud2.save()
    stud3 = models.Student.objects.create(name="GoodStudent3")
    stud3.classes.add(class1)
    stud3.save()
    stud4 = models.Student.objects.create(name="GoodStudent4")
    stud4.classes.add(class1,class2)
    stud4.save()

    stud5 = models.Student.objects.create(name="BadStudent1")
    stud5.classes.add(class1,class2)
    stud5.save()
    stud6 = models.Student.objects.create(name="BadStudent2")
    stud6.classes.add(class1,class2)
    stud6.save()
    stud7 = models.Student.objects.create(name="BadStudent3")
    stud7.classes.add(class2)
    stud7.save()

    # Populate the Person Table
    person1 = models.Person.objects.create(name="Jimmy")
    person2 = models.Person.objects.create(name="Joe")
    person3 = models.Person.objects.create(name="Jill")

    person1.friends.add(person2)
    person3.friends.add(person2)

    # Populate the Country Table
    coolVille = models.Country.objects.create(name="CoolVille")
    lameZone = models.Country.objects.create(name="LameZone")

    # Populate the President Table
    models.President.objects.create(name="Jonny Chill",country=coolVille)
    models.President.objects.create(name="Loser McGuy",country=lameZone)
