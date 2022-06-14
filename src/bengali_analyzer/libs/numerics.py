class NumericAnalyzer:
    def __init__(
        self,
        numeric_digit,
        numeric_literals,
        numeric_weights,
        numeric_suffixes,
        numeric_prefixes,
        numeric_months,
        numeric_special_cases,
        numeric_days,
    ):
        self.digits = numeric_digit
        self.literals = numeric_literals
        self.numerical_suffix = numeric_suffixes
        self.numerical_prefix = numeric_prefixes
        self.numerical_weight = numeric_weights
        self.months = numeric_months
        self.time_expressions = numeric_months
        self.special_cases = numeric_special_cases
        self.days = numeric_days

    def validate_digit(self, tokens, text, text_copy):
        digit = ""
        flag = False
        for char in text_copy:
            if char in self.digits:
                digit += char
                flag = True
        if flag:
            tokens[text]["numeric"]["digit"] = digit
        return flag

    def validate_literal(self, tokens, text, text_copy):
        if text_copy in self.literals:
            tokens[text]["numeric"]["literal"] = text_copy
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
            text_copy = text_copy[: -len(longest_suffix)]

        weight = ""
        for x in self.numerical_weight:
            if text_copy.endswith(x):
                weight = x
                break

        verdict = False

        if weight:
            text_copy = text_copy[: -len(weight)]

        if self.validate_literal(tokens, text, text_copy) or self.validate_digit(
            tokens, text, text_copy
        ):
            verdict = True

        if suffix and verdict:
            tokens[text]["numeric"]["suffix"] = suffix
        if weight and verdict:
            tokens[text]["numeric"]["weight"] = weight

        return verdict

    def get_numerics(self, tokens):
        flags = []
        for key, value in tokens.items():
            if self.validate_numeric(tokens, key):
                flags.extend(tokens[key]["global_index"])

        return flags
