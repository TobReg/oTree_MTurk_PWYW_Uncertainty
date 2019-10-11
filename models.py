from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import itertools

author = 'Elisa Hofmann'

doc = """
Pay-What-You-Want and Uncertainty
"""


class Constants(BaseConstants):
    name_in_url = 'MTurk_Unc_PWYW'
    players_per_group = 4
    num_rounds = 1
    treatment = 3
    endowment = c(10)
    prod_cost = c(3)
    role_desc = {'seller': 'S',
                 'buyer': 'B'}
    wtp1 = 3.22
    wtp2 = 5.89
    wtp3 = 8.81


class Subsession(BaseSubsession):

    # treatment = models.StringField(initi='DCertQCert')

    def creating_session(self):
        for p in self.get_players():
            if p.id_in_group == 2:
                p.private_value = Constants.wtp1
            elif p.id_in_group == 3:
                p.private_value = Constants.wtp2
            elif p.id_in_group == 4:
                p.private_value = Constants.wtp3

        self.group_randomly(fixed_id_in_group=True)

 #   class Subsession(BaseSubsession):
 #       def creating_session(self):
 #           treatments = itertools.cycle([1, 2, 3, 4])
 #           for g in self.get_groups():
 #               g.treatment = next(treatments)

class Group(BaseGroup):
 #   treatment = models.IntegerField()
 #   demand_certainty = models.BooleanField()
 #   quality_certainty = models.BooleanField()

    s_choice_PWYW_FP = models.IntegerField(choices=[(0, "Pay-What-You-Want"), (1, "Fixed Price")],
                                           label='Which pricing mechanism do you choose for your product',
                                           widget=widgets.RadioSelectHorizontal)

    s_decision_price_FP = models.IntegerField(min=0,
                                              max=Constants.endowment,
                                              label='Which price do you choose for your product?')

    total_payments = models.IntegerField(min=0,
                                          max=3*Constants.endowment,
                                          label='Total payments for the product')

#    mechanism = models.IntegerField()
#    fixed_price = models.IntegerField()
#    bought = models.IntegerField()
#    payment = models.IntegerField()
    purchases = models.IntegerField()

    def set_payoffs(self):

        print('in payoff function')

        seller = self.get_player_by_role('seller')
        buyer = self.get_player_by_role('buyer')
        b1 = self.get_player_by_id(2)
        b2 = self.get_player_by_id(3)
        b3 = self.get_player_by_id(4)
        self.purchases = b1.b_decision_buy + b2.b_decision_buy + b3.b_decision_buy

        if buyer.b_decision_buy == 0:
            buyer.payoff = 0
        elif buyer.b_decision_buy == 1 and self.s_choice_PWYW_FP == 0:
            buyer.payoff = buyer.private_value - buyer.b_decision_price_PWYW
        elif buyer.b_decision_buy == 1 and self.s_choice_PWYW_FP == 1:
            buyer.payoff = buyer.private_value - self.s_decision_price_FP

        if b2.b_decision_buy == 0:
            b2.payoff = 0
        elif b2.b_decision_buy == 1 and self.s_choice_PWYW_FP == 0:
            b2.payoff = b2.private_value - b2.b_decision_price_PWYW
        elif b2.b_decision_buy == 1 and self.s_choice_PWYW_FP == 1:
            b2.payoff = b2.private_value - self.s_decision_price_FP

        if b3.b_decision_buy == 0:
            b3.payoff = 0
        elif b3.b_decision_buy == 1 and self.s_choice_PWYW_FP == 0:
            b3.payoff = b3.private_value - b3.b_decision_price_PWYW
        elif b3.b_decision_buy == 1 and self.s_choice_PWYW_FP == 1:
            b3.payoff = b3.private_value - self.s_decision_price_FP

#        print('paid price', buyer.b_decision_price_PWYW)
#        print('id', buyer.id_in_group)

        if self.s_choice_PWYW_FP == 0:
            self.total_payments = b1.b_decision_price_PWYW + b2.b_decision_price_PWYW + b3.b_decision_price_PWYW
        elif self.s_choice_PWYW_FP == 1:
            self.total_payments = (b1.b_decision_buy + b2.b_decision_buy + b3.b_decision_buy) * self.s_decision_price_FP

        if self.s_choice_PWYW_FP == 0:
            seller.payoff = b1.b_decision_price_PWYW + b2.b_decision_price_PWYW + b3.b_decision_price_PWYW - Constants.prod_cost
        elif self.s_choice_PWYW_FP == 1:
            seller.payoff = (b1.b_decision_buy + b2.b_decision_buy + b3.b_decision_buy) * self.s_decision_price_FP - Constants.prod_cost

class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'seller'
        return 'buyer'
    pass

    question1 = models.IntegerField(choices=[(0, "wrong"), (1, "correct")],
                                         label='Is this statement correct or wrong?',
                                         widget=widgets.RadioSelectHorizontal)

    b_decision_buy = models.IntegerField(choices=[(0, "No"), (1, "Yes")],
                                         label='Do you want to buy the product?',
                                         widget=widgets.RadioSelectHorizontal)

    b_decision_price_PWYW = models.IntegerField(min=0, max=Constants.endowment,
                                                label='How much do you want to pay for the product?')

    private_value = models.FloatField(doc="How much the buyer values the item")

    prod_cost = models.IntegerField(min=2, max=2, label="How high are the production costs for the seller")