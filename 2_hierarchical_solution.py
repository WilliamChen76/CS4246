"""
Assignment 1 - Problem 2 hierarchical planning testing script.

* Group Member 1:
    - Name:
    - Student ID:

* Group Member 2:
    - Name:
    - Student ID:
"""

### AFTER YOU COMPLETE THE 2_hierarchical.ipynb, COPY YOUR CODES HERE FOR OUR EVALUATION ###

import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.model.htn import *


def generate_hierarchical(NUM_FLOOR, NUM_PEOPLE, FLOOR_LIST):
    problem = HierarchicalProblem('ElevatorHTNProblem')

    Loc = UserType("Loc")
    Floor = UserType('Floor', father=Loc)
    Elevator = UserType('Elevator', father=Loc)
    Person = UserType('Person')

    # Add objects (floors and people)
    floors = [Object(f'floor{i}', Floor) for i in range(NUM_FLOOR)]
    people = [Object(f'person{i}', Person) for i in range(NUM_PEOPLE)]
    elevator = [Object('elevator', Elevator)]
    problem.add_objects(floors + people + elevator)

    at_person = Fluent('at_person', Loc, person=Person)
    at_elevator = Fluent('at_elevator', Floor, elevator=Elevator)
    elevator_door_open = Fluent('elevator_door_open', BoolType(), elevator=Elevator)

    problem.add_fluent(at_person)
    problem.add_fluent(at_elevator)
    problem.add_fluent(elevator_door_open)

    for i in range(NUM_PEOPLE):
        problem.set_initial_value(at_person(people[i]), floors[int(FLOOR_LIST[i])])

    problem.set_initial_value(at_elevator(elevator[0]), floors[0])
    problem.set_initial_value(elevator_door_open(elevator[0]), False)

    move_elevator = InstantaneousAction('move_elevator', elevator=Elevator, start=Floor, end=Floor)

    # COPY-FLAG-1-START

    # COPY-FLAG-1-END

    enter_elevator = InstantaneousAction('enter_elevator', elevator=Elevator, person=Person, floor=Floor)

    # COPY-FLAG-2-START

    # COPY-FLAG-2-END

    exit_elevator = InstantaneousAction('exit_elevator', elevator=Elevator, person=Person, floor=Floor)

    # COPY-FLAG-3-START

    # COPY-FLAG-3-END

    open_door = InstantaneousAction('open_door', elevator=Elevator)

    # COPY-FLAG-4-START

    # COPY-FLAG-4-END

    close_door = InstantaneousAction('close_door', elevator=Elevator)

    # COPY-FLAG-5-START

    # COPY-FLAG-5-END

    problem.add_action(move_elevator)
    problem.add_action(enter_elevator)
    problem.add_action(exit_elevator)
    problem.add_action(open_door)
    problem.add_action(close_door)

    def method_transport_person(transport_person):
        method = Method('method_transport_person', elevator=Elevator, person=Person, original_floor=Floor,
                        start_floor=Floor, end_floor=Floor)
        method.set_task(transport_person, method.person, method.end_floor)
        # Conditions for the method to be applicable
        method.add_precondition(Equals(at_person(method.person), method.start_floor))
        method.add_precondition(Equals(at_elevator(method.elevator), method.original_floor))
        method.add_precondition(Not(Equals(at_person(method.person), method.end_floor)))
        method.add_precondition(Not(Equals(at_elevator(method.elevator), method.start_floor)))
        method.add_precondition(Not(elevator_door_open(method.elevator)))
        # this method decomposed into a sequence of 8 subtasks
        t1 = method.add_subtask(move_elevator, method.elevator, method.original_floor, method.start_floor)
        t2 = method.add_subtask(open_door, method.elevator)
        t3 = method.add_subtask(enter_elevator, method.elevator, method.person, method.start_floor)
        t4 = method.add_subtask(close_door, method.elevator)
        t5 = method.add_subtask(move_elevator, method.elevator, method.start_floor, method.end_floor)
        t6 = method.add_subtask(open_door, method.elevator)
        t7 = method.add_subtask(exit_elevator, method.elevator, method.person, method.end_floor)
        t8 = method.add_subtask(close_door, method.elevator)
        method.set_ordered(t1, t2, t3, t4, t5, t6, t7, t8)
        # print(method)

        return method

    def method_transport_noop(transport_person):
        method = Method('method_transport_noop', elevator=Elevator, person=Person, start_floor=Floor, end_floor=Floor)

        method.set_task(transport_person, method.person, method.end_floor)
        # Conditions for the method to be applicable
        method.add_precondition(Equals(at_person(method.person), method.start_floor))
        method.add_precondition(Equals(at_person(method.person), method.end_floor))
        # print(method)
        return method

    transport_person = problem.add_task('transport_person', person=Person, end_floor=Floor)

    problem.add_method(method_transport_person(transport_person))
    problem.add_method(method_transport_noop(transport_person))

    for p in people:
        # COPY-FLAG-6-START


        # COPY-FLAG-6-END
