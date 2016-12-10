import re

ASSIGNMENT_REGEX = re.compile('value (\d+) goes to bot (\d+)')
MOVE_REGEX = re.compile('bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')
BOT, OUT = 'bot', 'output'


class Bot:
    def __init__(self, bot_id):
        self._bot_id = bot_id
        self._values = []
        self._low_target = None
        self._high_target = None

    def add_value(self, value):
        self._values.append(value)

    def set_targets(self, low_target, high_target):
        self._low_target = low_target
        self._high_target = high_target

    @property
    def has_two_values(self):
        return len(self._values) == 2

    def run(self):
        if not self.has_two_values:
            raise RuntimeError(self)
        min_val, max_val = sorted(self._values)
        if min_val == 17 and max_val == 61:
            print("Bot {} compares {} to {}".format(self._bot_id, min_val, max_val))
        self._low_target.add_value(min_val)
        self._high_target.add_value(max_val)
        self._values = []

    def __str__(self):
        return "<Bot {}>".format(self._bot_id)

    __repr__ = __str__


class Output:
    def __init__(self, output_id):
        self._output_id = output_id
        self._values = []

    def add_value(self, value):
        self._values.append(value)

    @property
    def value(self):
        assert len(self._values) == 1
        return self._values[0]

    def __str__(self):
        return "<Output {}: {}>".format(self._output_id, self._values)

    __repr__ = __str__


class BotNetwork:
    def __init__(self):
        self._bots = {}
        self._outputs = {}

    def update(self, rule_line):
        assignment_match = ASSIGNMENT_REGEX.match(rule_line)
        if assignment_match:
            self._update_assignments(assignment_match)
        move_match = MOVE_REGEX.match(rule_line)
        if move_match:
            self._update_move_rules(move_match)

    def _update_assignments(self, match):
        value, bot_id = match.groups()
        value = int(value)
        bot_id = int(bot_id)
        self._get_or_create_bot(bot_id).add_value(value)

    def _update_move_rules(self, match):
        bot_id, low_dst_type, low_dst, high_dst_type, high_dst = match.groups()
        bot_id = int(bot_id)
        low_dst = int(low_dst)
        high_dst = int(high_dst)

        low_dst_obj = self._get_or_create_destination_object(low_dst_type, low_dst)
        high_dst_obj = self._get_or_create_destination_object(high_dst_type, high_dst)
        self._get_or_create_bot(bot_id).set_targets(low_dst_obj, high_dst_obj)

    def _get_or_create_bot(self, bot_id):
        if bot_id not in self._bots:
            self._bots[bot_id] = Bot(bot_id)
        return self._bots[bot_id]

    def _get_or_create_output(self, output_id):
        if output_id not in self._outputs:
            self._outputs[output_id] = Output(output_id)
        return self._outputs[output_id]

    def _get_or_create_destination_object(self, destination_type, destination_id):
        if destination_type == OUT:
            return self._get_or_create_output(destination_id)
        elif destination_type == BOT:
            return self._get_or_create_bot(destination_id)
        else:
            raise RuntimeError(destination_type)

    def run(self):
        while True:
            for b in self._bots.values():
                if b.has_two_values:
                    b.run()
                    break
            else:
                return

    @property
    def outputs(self):
        return self._outputs


n = BotNetwork()
with open('../data/day10.txt') as f:
    for line in f:
        n.update(line)
n.run()

o = n.outputs
print(o[0].value * o[1].value * o[2].value)
