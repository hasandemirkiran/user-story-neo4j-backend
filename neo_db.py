from py2neo import Graph, Node, Relationship, NodeMatcher
import csv

graph = Graph("bolt://localhost:7687", auth=("neo4j", "hasan"))


def create_graph():

    with open('./files/separated_sentences.csv', encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            node = Node('UserStory', name=row['ID'], actionRole=row['ActionRole'], actionObject=row[
                'ActionObject'], actionPlace=row['ActionPlace'], actionTool=row['ActionTool'], actionTime=row[
                'ActionTime'], action=row['Action'], benefitObject=row['BenefitObject'], benefitPlace=row['BenefitPlace'],
                benefitTool=row['BenefitTool'], benefitTime=row['BenefitTime'], benefitAction=row['BenefitAction'])

            node_action = Node('Action', name=row['Action'])
            node_action_role = Node('ActionRole', name=row['ActionRole'])
            node_action_object = Node('ActionObject', name=row['ActionObject'])
            node_action_place = Node('ActionPlace', name=row['ActionPlace'])
            node_action_time = Node('ActionTime', name=row['ActionTime'])
            node_action_tool = Node('ActionTool', name=row['ActionTool'])

            node_benefit_action = Node(
                'BenefitAction', name=row['BenefitAction'])
            node_benefit_object = Node(
                'BenefitObject', name=row['BenefitObject'])
            node_benefit_place = Node('BenefitPlace', name=row['BenefitPlace'])
            node_benefit_time = Node('BenefitTime', name=row['BenefitTime'])
            node_benefit_tool = Node('BenefitTool', name=row['BenefitTool'])

            ACTION = Relationship.type('ACTION')
            ACTIONROLE = Relationship.type('ACTIONROLE')
            ACTIONOBJECT = Relationship.type('ACTIONOBJECT')
            ACTIONPLACE = Relationship.type('ACTIONPLACE')
            ACTIONTIME = Relationship.type('ACTIONTIME')
            ACTIONTOOL = Relationship.type('ACTIONTOOL')

            BENEFITACTION = Relationship.type('BENEFITACTION')
            BENEFITOBJECT = Relationship.type('BENEFITOBJECT')
            BENEFITPLACE = Relationship.type('BENEFITPLACE')
            BENEFITTIME = Relationship.type('BENEFITTIME')
            BENEFITTOOL = Relationship.type('BENEFITTOOL')

            graph.merge(ACTION(node, node_action), 'UserStory', 'name')
            graph.merge(ACTIONROLE(node, node_action_role),
                        'UserStory', 'name')
            graph.merge(ACTIONOBJECT(node, node_action_object),
                        'UserStory', 'name')
            graph.merge(ACTIONPLACE(node, node_action_place),
                        'UserStory', 'name')
            graph.merge(ACTIONTIME(node, node_action_time),
                        'UserStory', 'name')
            graph.merge(ACTIONTOOL(node, node_action_tool),
                        'UserStory', 'name')

            graph.merge(BENEFITACTION(node, node_benefit_action),
                        'UserStory', 'name')
            graph.merge(BENEFITOBJECT(node, node_benefit_object),
                        'UserStory', 'name')
            graph.merge(BENEFITPLACE(node, node_benefit_place),
                        'UserStory', 'name')
            graph.merge(BENEFITTIME(node, node_benefit_time),
                        'UserStory', 'name')
            graph.merge(BENEFITTOOL(node, node_benefit_tool),
                        'UserStory', 'name')

    # print(list(matcher.match('UserStory').where(name='US1')))


def get_nodes_specific(node_name):
    matcher = NodeMatcher(graph)
    return list(matcher.match(node_name))
