class NumericAnalyzer:
    def __init__(self):
        self.digits = {'০', '১', '২', '৩', '৪', '৫', '৬', '৭', '৮', '৯'}
        self.literals = {'এক', 'দুই', 'তিন', 'চার', 'পাঁচ', 'ছয়', 'সাত', 'আট', 'নয়', 'দশ', 'এগারো', 'বার', 'তের',
                         'চৌদ্দ', 'পনের', 'ষোল', 'সতের', 'আঠার', 'উনিশ', 'বিশ', 'একুশ', 'বাইশ', 'তেইশ', 'চব্বিশ',
                         'পঁচিশ', 'ছাব্বিশ', 'সাতাশ', 'আঠাশ', 'ঊনত্রিশ', 'ত্রিশ', 'একত্রিশ', 'বত্রিশ', 'তেত্রিশ',
                         'চৌত্রিশ', 'পঁয়ত্রিশ', 'ছত্রিশ', 'সাঁইত্রিশ', 'আটত্রিশ', 'ঊনচল্লিশ', 'চল্লিশ', 'একচল্লিশ',
                         'বিয়াল্লিশ', 'তেতাল্লিশ', 'চুয়াল্লিশ', 'পঁয়তাল্লিশ', 'ছেচল্লিশ', 'সাতচল্লিশ', 'আটচল্লিশ',
                         'ঊনপঞ্চাশ', 'পঞ্চাশ', 'একান্ন', 'বায়ান্ন', 'তিপ্পান্ন', 'চুয়ান্ন', 'পঞ্চান্ন', 'ছাপ্পান্ন',
                         'সাতান্ন', 'আটান্ন', 'ঊনষাট', 'ষাট', 'একষট্টি', 'বাষট্টি', 'তেষট্টি', 'চৌষট্টি', 'পঁয়ষট্টি',
                         'ছেষট্টি', 'সাতষট্টি', 'আটষট্টি', 'ঊনসত্তর', 'সত্তর', 'একাত্তর', 'বাহাত্তর', 'তিয়াত্তর',
                         'চুয়াত্তর', 'পঁচাত্তর', 'ছিয়াত্তর', 'সাতাত্তর', 'আটাত্তর', 'ঊনআশি', 'আশি', 'একাশি', 'বিরাশি',
                         'তিরাশি', 'চুরাশি', 'পঁচাশি', 'ছিয়াশি', 'সাতাশি', 'আটাশি', 'ঊননব্বই', 'নব্বই', 'একানব্বই',
                         'বিরানব্বই', 'তিরানব্বই', 'চুরানব্বই', 'পঁচানব্বই', 'ছিয়ানব্বই', 'সাতানব্বই', 'আটানব্বই',
                         'নিরানব্বই'}
        self.numerical_suffix = {'বার', 'টি', 'টা', 'ে', 'তে', 'টিবার', 'টাবার'}
        self.numerical_weight = {'কোটি', 'লক্ষ', 'হাজার', 'শত', 'শো'}
        self.months = {}
        self.time_expressions = {}

    def validate_digit(self, tokens, text, text_copy):
        if text_copy in self.digits:
            tokens[text]['Numeric']['Digit'] = text_copy
            return True
        return False

    def validate_literal(self, tokens, text, text_copy):
        if text_copy in self.literals:
            tokens[text]['Numeric']['Literal'] = text_copy
            return True
        return False

    def validate_numeric(self, tokens, text):
        suffix = []
        for x in self.numerical_suffix:
            if text.endswith(x):
                suffix.append(x)

        text_copy = text

        if suffix:
            longest_suffix = max(suffix, key=len)
            text_copy = text_copy[:- len(longest_suffix)]

        weight = ""
        for x in self.numerical_weight:
            if text_copy.endswith(x):
                weight = x
                break

        verdict = False

        if weight:
            text_copy = text_copy[:- len(weight)]
            tokens[text]['Numeric']['Weight'] = weight
            verdict = True

        if weight and suffix:
            tokens[text]['Numeric']['Suffix'] = suffix

        if self.validate_literal(tokens, text, text_copy) or self.validate_literal(tokens, text, text_copy):
            verdict = True

        if suffix and verdict:
            tokens[text]['Numeric']['Suffix'] = suffix

        return verdict

    def get_numerics(self, tokens):
        flags = []
        for key, value in tokens.items():
            if self.validate_numeric(tokens, key):
                flags.extend(tokens[key]["Global_Index"])

        return flags
