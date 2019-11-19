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
    treatment = 2
    endowment = 10
    prod_cost = 3
    role_desc = {'seller': 'S',
                 'buyer': 'B'}
    wtp1 = 3.22
    wtp2 = 5.89
    wtp3 = 8.81

    instructions_template = 'MTurk_Unc_PWYW/Instructions2.html'
    instructions_decision = 'MTurk_Unc_PWYW/InstrucDecisionSituation.html'


class Subsession(BaseSubsession):

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

    s_choice_PWYW_FP = models.BooleanField(choices=[(0, "Pay-What-You-Want"), (1, "Fixed Price")],
                                           label='Which pricing mechanism do you choose for your product?',
                                           widget=widgets.RadioSelectHorizontal)

    s_decision_price_FP = models.FloatField(min=0,
                                              max=Constants.endowment,
                                              label='Which price do you choose for your product?')

    total_payments = models.FloatField(min=0,
                                          max=3*Constants.endowment,
                                          label='Total payments for the product')

#    mechanism = models.IntegerField()
#    fixed_price = models.IntegerField()
#    bought = models.IntegerField()
#    payment = models.IntegerField()
    purchases = models.IntegerField()
    b1payment = models.FloatField()
    b2payment = models.FloatField()
    b3payment = models.FloatField()

    def set_payoffs(self):

        print('in payoff function')

        seller = self.get_player_by_role('seller')
        buyer = self.get_player_by_role('buyer')
        b1 = self.get_player_by_id(2)
        b2 = self.get_player_by_id(3)
        b3 = self.get_player_by_id(4)
        self.purchases = b1.b_decision_buy + b2.b_decision_buy + b3.b_decision_buy

        if self.s_choice_PWYW_FP == 0 and b1.b_decision_buy == 0:
            b1.b_decision_price_PWYW = 0
        if self.s_choice_PWYW_FP == 0 and b2.b_decision_buy == 0:
            b2.b_decision_price_PWYW = 0
        if self.s_choice_PWYW_FP == 0 and b3.b_decision_buy == 0:
            b3.b_decision_price_PWYW = 0

        if self.s_choice_PWYW_FP == 0:
            self.b1payment = b1.b_decision_price_PWYW
            self.b2payment = b2.b_decision_price_PWYW
            self.b3payment = b3.b_decision_price_PWYW
        elif self.s_choice_PWYW_FP == 1:
            self.b1payment = b1.b_decision_buy * self.s_decision_price_FP
            self.b2payment = b2.b_decision_buy * self.s_decision_price_FP
            self.b3payment = b3.b_decision_buy * self.s_decision_price_FP

        if b1.b_decision_buy == 0:
            b1.payoff = 0
        elif b1.b_decision_buy == 1 and self.s_choice_PWYW_FP == 0:
            b1.payoff = b1.private_value - b1.b_decision_price_PWYW
        elif b1.b_decision_buy == 1 and self.s_choice_PWYW_FP == 1:
            b1.payoff = b1.private_value - self.s_decision_price_FP

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
#    pass

    question1 = models.BooleanField(choices=[(0, "right"), (1, "wrong")],
                                         label='"As seller you can decide on your own, which pricing mechanism you use to sell your product."',
                                         widget=widgets.RadioSelectHorizontal)

    question2 = models.BooleanField(choices=[(0, "right"), (1, "wrong")],
                                         label='"If the seller choses PWYW (pay what you want) as pricing mechanism, the buyers can decide on their own how much to pay for the product."',
                                         widget=widgets.RadioSelectHorizontal)

    question3s = models.IntegerField(min=-3, max=27, label="Please calculate the payoff for the seller and enter the result into the field below.")

    question3b1 = models.IntegerField(min=-3, max=5, label="Enter the payoff of buyer 1 into the field below.")

    question3b2 = models.IntegerField(min=-3, max=27, label="Please calculate the payoff for buyer 2 and enter the result into the field below.")

    question3b3 = models.IntegerField(min=-3, max=27, label="Please calculate the payoff for buyer 3 and enter the result into the field below.")

    question4 = models.IntegerField(min=-3, max=27, label="Please calculate the payoff for buyer 3 and enter the results into the respective field.")

    b_decision_buy = models.BooleanField(choices=[(0, "No"), (1, "Yes")],
                                         label='Do you want to buy the product?',
                                         widget=widgets.RadioSelectHorizontal)

    private_value = models.FloatField(min=2, max=10, doc="How much the buyer values the item")
#    private_value = self.subsession.private_value

    b_decision_price_PWYW = models.FloatField(min=0, max=Constants.endowment,
                                                label='How much do you want to pay for the product?')

    survey_easy_difficult = models.IntegerField(choices=[(1, "Very easy"), (2, ""), (3, ""), (4, ""),
                                        (5, ""), (6, ""), (7, "Very complicated")],
                                         label='Did you find the experiment rather easy or difficult?',
                                         widget=widgets.RadioSelectHorizontal)

    survey_risk = models.IntegerField(choices=[(1, "Very risk averse"), (2, ""), (3, ""), (4, ""),
                                            (5, ""), (6, ""), (7, ""), (8, ""), (9, ""), (10, "Very risk seeking")],
                                   label='In general, how do you evaluate your own risk preferences?',
                                   widget=widgets.RadioSelectHorizontal)

    age = models.IntegerField(min=18,
                              max=120,
                              label='How old are you?')

    strategy_seller = models.LongStringField(label='If you have been a seller: Please describe, why you decided for a "Fixed Price" or for "PWYW" (pay what you want):')

    strategy_buyer = models.LongStringField(label='If you have been a buyer: Please describe, what influenced your decision for the PWYW price:')

    gender = models.IntegerField(choices=[(0, "Male"), (1, "Female")],
                                  label='Which gender do you identify with?')

    feedback = models.LongStringField(label='Do you have any further comments on the experiment?')
