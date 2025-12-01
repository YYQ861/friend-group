class Person:
    """A class to represent an individual."""

    def __init__(self, name, age, job):
        """Create a new Person with the given name, age and job."""
        self.name = name
        self.age = age
        self.job = job


class Group:
    """A class that represents a group of individuals and their connections."""

    def __init__(self):
        """Create an empty group."""
        # 保存所有成员对象
        self.members = []          # list[Person]
        # 保存关系：名字 -> { 另一个名字: 关系 }
        self.connections = {}      # dict[str, dict[str, str]]

    def size(self):
        """Return how many people are in the group."""
        return len(self.members)

    def contains(self, name):
        """Check whether the group contains a person with the given name.
        Useful to throw errors if we try to add a person who already exists or forget someone.
        """
        return any(member.name == name for member in self.members)

    def add_person(self, name, age, job):
        """Add a new person with the given characteristics to the group."""
        if self.contains(name):
            raise ValueError(f"{name} is already in the group")
        self.members.append(Person(name, age, job))
        # 初始化这个人的关系字典（现在还是空的）
        self.connections[name] = {}

    def number_of_connections(self, name):
        """Find the number of connections that a person in the group has"""
        if name not in self.connections:
            raise ValueError(f"{name} is not in the group")
        return len(self.connections[name])

    def connect(self, name1, name2, relation, reciprocal=True):
        """Connect two given people in a particular way.
        Optional reciprocal: If true, will add the relationship from name2 to name1 as well
        """
        if not self.contains(name1) or not self.contains(name2):
            raise ValueError("Both people must be in the group before connecting them")

        # 确保两个名字在 connections 里都有 key
        self.connections.setdefault(name1, {})
        self.connections.setdefault(name2, {})

        # name1 -> name2
        self.connections[name1][name2] = relation

        # reciprocal=True 时，再加一条反向关系
        if reciprocal:
            self.connections[name2][name1] = relation

    def forget(self, name1, name2):
        """Remove the connection between two people."""
        # 和前面字典版本一样：两边都尝试删掉
        if name1 in self.connections:
            self.connections[name1].pop(name2, None)
        if name2 in self.connections:
            self.connections[name2].pop(name1, None)

    def average_age(self):
        """Compute the average age of the group's members."""
        all_ages = [person.age for person in self.members]
        return sum(all_ages) / self.size()


if __name__ == "__main__":
    # Start with an empty group...
    my_group = Group()

    # ...then add the group members one by one...
    my_group.add_person("Jill", 26, "biologist")
    my_group.add_person("Zalika", 28, "artist")
    my_group.add_person("John", 27, "writer")
    my_group.add_person("Nash", 34, "chef")

    # ...then their connections（照 Stage 1/2 的数据翻译过来）

    # Jill <-> Zalika : friend（双向）
    my_group.connect("Jill", "Zalika", "friend")

    # Jill <-> John : partner（双向）
    my_group.connect("Jill", "John", "partner")

    # Nash -> John : cousin（单向）
    my_group.connect("Nash", "John", "cousin", reciprocal=False)

    # Nash -> Zalika : landlord（单向）
    my_group.connect("Nash", "Zalika", "landlord", reciprocal=False)

    # ... then forget Nash and John's connection
    my_group.forget("Nash", "John")

    print("DEBUG members:", [p.name for p in my_group.members])

    assert my_group.contains("John"), "John should be in the group"
    assert my_group.size() == 4, "Group should have 4 members"
    assert my_group.average_age() == 28.75, "Average age of the group is incorrect!"
    assert my_group.number_of_connections("Nash") == 1, "Nash should only have one relation"
    print("All assertions have passed!")

