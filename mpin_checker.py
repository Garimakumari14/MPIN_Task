import datetime

class MPINEvaluator:
    
    COMMON_MPINS = {
        "1234", "1111", "0000", "9999", "1122", "1212", "7777", "1004", "2000", "2222",
        "123456", "000000", "111111", "999999", "654321", "234567", "555555", "888888"
    }
   
    KEYBOARD_PATTERNS = {
        "1234", "2345", "3456", "4567", "5678", "6789", "7890", 
        "4321", "5432", "6543", "7654", "8765", "9876", "0987",  
        "1470", "2580", "3690",  
        "159", "357",  
        "1010", "1212", "1313", 
        "0101", "1001",
        "1100", "2200", "3300", 
        "1999", "2000", "2001", 
        "12345", "67890", 
        "123456", "234567", "345678", "456789", "567890", 
        "654321", "765432", "876543", "987654", "098765" 
    }

    def __init__(self, mpin: str, dob_self=None, dob_spouse=None, anniversary=None):
        self.mpin = mpin
        self.dob_self = dob_self
        self.dob_spouse = dob_spouse
        self.anniversary = anniversary
        self.weak_reasons = [] 

    def _parse_date(self, date_str):
        """Safely parses a date string into a datetime.date object."""
        if date_str:
            try:
                return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                return None
        return None

    def _is_common_mpin(self):
        """Checks if the MPIN is in a list of commonly used ones."""
        return self.mpin in self.COMMON_MPINS

    def _is_sequential(self):
        """Checks for simple ascending or descending sequences of at least 3 digits."""
        for i in range(len(self.mpin) - 2): 
            sub = self.mpin[i:i+3]
            
            if all(int(sub[j]) == int(sub[j-1]) + 1 for j in range(1, len(sub))):
                return True
            
            if all(int(sub[j]) == int(sub[j-1]) - 1 for j in range(1, len(sub))):
                return True
        return False

    def _is_repeating_digits(self):
        """Checks if the MPIN consists of only repeating digits (e.g., 1111, 222222)."""
        return len(set(self.mpin)) == 1
    
    def _is_repeating_patterns(self):
        """Checks for repeating patterns like '1212', '2323' or '123123'."""
        length = len(self.mpin)
        if length % 2 == 0 and length >= 4:
            half = length // 2
            if self.mpin[:half] == self.mpin[half:]:
                return True
        if length % 3 == 0 and length >= 6:
            third = length // 3
            if self.mpin[:third] == self.mpin[third:2*third] == self.mpin[2*third:]:
                return True
        return False

    def _is_keyboard_pattern(self):
        """Checks if the MPIN matches common keyboard patterns."""
        return self.mpin in self.KEYBOARD_PATTERNS or any(p in self.mpin for p in self.KEYBOARD_PATTERNS if len(p) < len(self.mpin))

    def _is_date_related(self):
        """Checks if the MPIN is directly related to provided demographic dates."""
        dates_to_check = []
        if self.dob_self: dates_to_check.append(self._parse_date(self.dob_self))
        if self.dob_spouse: dates_to_check.append(self._parse_date(self.dob_spouse))
        if self.anniversary: dates_to_check.append(self._parse_date(self.anniversary))

        for date_obj in dates_to_check:
            if not date_obj: continue 

            
            date_formats = {
                date_obj.strftime("%d%m"): "DDMM", 
                date_obj.strftime("%m%d"): "MMDD", 
                date_obj.strftime("%y%m"): "YYMM", 
                date_obj.strftime("%m%y"): "MMYY",
                date_obj.strftime("%Y"): "YYYY",   
                date_obj.strftime("%d%m%y"): "DDMMYY", 
                date_obj.strftime("%m%d%y"): "MMDDYY", 
                date_obj.strftime("%y%m%d"): "YYMMDD", 
                str(date_obj.year) + date_obj.strftime("%m"): "YYYYMM", 
                str(date_obj.year) + date_obj.strftime("%d"): "YYYYDD", 
                date_obj.strftime("%m") + str(date_obj.year): "MMYYYY", 
                date_obj.strftime("%d") + str(date_obj.year): "DDYYYY", 
            }
            
            for pattern_value, description in date_formats.items():
                if len(pattern_value) == len(self.mpin) and self.mpin == pattern_value:
                    if description.startswith("DDMM"):
                        self.weak_reasons.append(f"Uses your {date_obj.year} date (DDMM, {date_obj.strftime('%d%m')}).")
                    elif description.startswith("MMDD"):
                         self.weak_reasons.append(f"Uses your {date_obj.year} date (MMDD, {date_obj.strftime('%m%d')}).")
                    elif description.startswith("YYMM"):
                        self.weak_reasons.append(f"Uses your {date_obj.year} date (YYMM, {date_obj.strftime('%y%m')}).")
                    elif description.startswith("YYYY"):
                        self.weak_reasons.append(f"Uses your {date_obj.year} as MPIN.")
                    elif description.startswith("DDMMYY"):
                        self.weak_reasons.append(f"Uses your {date_obj.year} date (DDMMYY, {date_obj.strftime('%d%m%y')}).")
                    elif description.startswith("MMDDYY"):
                        self.weak_reasons.append(f"Uses your {date_obj.year} date (MMDDYY, {date_obj.strftime('%m%d%y')}).")
                    elif description.startswith("YYMMDD"):
                        self.weak_reasons.append(f"Uses your {date_obj.year} date (YYMMDD, {date_obj.strftime('%y%m%d')}).")
                    elif description.startswith("YYYYMM"):
                         self.weak_reasons.append(f"Uses your {date_obj.year} date (YYYYMM, {date_obj.strftime('%Y%m')}).")
                    elif description.startswith("MMYYYY"):
                         self.weak_reasons.append(f"Uses your {date_obj.year} date (MMYYYY, {date_obj.strftime('%m%Y')}).")
                    elif description.startswith("DDYYYY"):
                         self.weak_reasons.append(f"Uses your {date_obj.year} date (DDYYYY, {date_obj.strftime('%d%Y')}).")
                    return True 
        return False

    def evaluate_strength(self):
        self.weak_reasons = [] 

        
        if self._is_common_mpin():
            self.weak_reasons.append("It is a very common and easily guessable MPIN.")
        
        if self._is_repeating_digits():
            self.weak_reasons.append("It consists of repeating digits (e.g., '1111').")
        
        if self._is_sequential():
            self.weak_reasons.append("It uses sequential digits (e.g., '1234' or '9876').")
            
        if self._is_repeating_patterns():
            self.weak_reasons.append("It uses repeating digit patterns (e.g., '1212', '123123').")

        if self._is_keyboard_pattern():
            self.weak_reasons.append("It matches common keyboard patterns (e.g., '2580', '1470').")

     
        self._is_date_related() 

        strength = "STRONG"
        if self.weak_reasons:
            if len(self.weak_reasons) >= 2 or any(r in self.weak_reasons for r in ["It is a very common and easily guessable MPIN.", "It consists of repeating digits (e.g., '1111')."]):
                strength = "WEAK"
            else:
                strength = "MODERATE"
        
        # Ensure a common MPIN is always marked WEAK
        if self._is_common_mpin():
            strength = "WEAK"
            if "It is a very common and easily guessable MPIN." not in self.weak_reasons:
                self.weak_reasons.insert(0, "It is a very common and easily guessable MPIN.")


        return {
            "MPIN": self.mpin,
            "Strength": strength,
            "Reasons": self.weak_reasons
        }

# --- Test Cases (for local testing of mpin_checker.py) ---
def run_tests():
    test_cases = [
        {"mpin": "1234", "expected_strength": "WEAK", "comment": "Common & Sequential"},
        {"mpin": "0201", "dob_self": "1998-01-02", "expected_strength": "WEAK", "comment": "DOB DDMM"},
        {"mpin": "9802", "dob_self": "1998-01-02", "expected_strength": "WEAK", "comment": "DOB YYMM"},
        {"mpin": "1998", "dob_self": "1998-01-02", "expected_strength": "WEAK", "comment": "DOB YYYY"},
        {"mpin": "1122", "expected_strength": "WEAK", "comment": "Common"},
        {"mpin": "0201", "dob_spouse": "1990-01-02", "expected_strength": "WEAK", "comment": "Spouse DOB DDMM"},
        {"mpin": "2107", "anniversary": "2020-07-21", "expected_strength": "WEAK", "comment": "Anniversary DDMM"},
        {"mpin": "9999", "expected_strength": "WEAK", "comment": "Repeating & Common"},
        {"mpin": "7777", "expected_strength": "WEAK", "comment": "Repeating & Common"},
        {"mpin": "210721", "anniversary": "2021-07-21", "expected_strength": "WEAK", "comment": "Anniversary DDMMYY"},
        {"mpin": "200000", "dob_self": "2000-01-01", "expected_strength": "WEAK", "comment": "Repeating & DOB YYYY00"},
        {"mpin": "8888", "expected_strength": "WEAK", "comment": "Repeating"},
        {"mpin": "2001", "dob_self": "2001-06-05", "expected_strength": "WEAK", "comment": "DOB YYYY"},
        {"mpin": "0506", "dob_self": "2001-06-05", "expected_strength": "WEAK", "comment": "DOB DDMM"},
        {"mpin": "6578", "expected_strength": "MODERATE", "comment": "Keyboard pattern sub-string"},
        {"mpin": "1004", "expected_strength": "WEAK", "comment": "Common"},
        {"mpin": "1212", "expected_strength": "WEAK", "comment": "Common & Repeating pattern"},
        {"mpin": "1111", "dob_spouse": "2011-11-11", "expected_strength": "WEAK", "comment": "Repeating & Common & Spouse DOB"},
        {"mpin": "020102", "dob_self": "1998-01-02", "expected_strength": "WEAK", "comment": "DOB MMDDYY from 1902-01-02 (adjust year for example)"},
        {"mpin": "123456", "expected_strength": "WEAK", "comment": "Common & Sequential"},
        {"mpin": "456789", "expected_strength": "WEAK", "comment": "Sequential"},
        {"mpin": "7890", "expected_strength": "WEAK", "comment": "Sequential & Keyboard"},
        {"mpin": "3579", "expected_strength": "MODERATE", "comment": "Simple pattern"},
        {"mpin": "98765", "expected_strength": "MODERATE", "comment": "Sequential part"},
        {"mpin": "543210", "expected_strength": "WEAK", "comment": "Sequential"},
        {"mpin": "707070", "expected_strength": "WEAK", "comment": "Repeating pattern"},
        {"mpin": "1357", "expected_strength": "MODERATE", "comment": "Odd sequence"},
        {"mpin": "4928", "expected_strength": "STRONG", "comment": "Truly strong"}, 
        {"mpin": "8765", "expected_strength": "WEAK", "comment": "Sequential"},
        {"mpin": "2580", "expected_strength": "WEAK", "comment": "Keyboard vertical"},
        {"mpin": "135792", "expected_strength": "STRONG", "comment": "Complex random"},
        {"mpin": "199912", "dob_self": "1999-12-25", "expected_strength": "WEAK", "comment": "DOB YYYYMM"},
        {"mpin": "0101", "dob_self": "2000-01-01", "expected_strength": "WEAK", "comment": "DOB DDMM"},
        {"mpin": "000001", "expected_strength": "MODERATE", "comment": "Starts with zeros, but not fully common"},
        {"mpin": "5238", "expected_strength": "STRONG", "comment": "Random"},
        {"mpin": "736452", "expected_strength": "STRONG", "comment": "Random"},
    ]

    print("\n🔍 MPIN Evaluation Results:")
    for i, case in enumerate(test_cases, 1):
      
        dob_self_val = case.get("dob_self")
        dob_spouse_val = case.get("dob_spouse")
        anniversary_val = case.get("anniversary")

        evaluator = MPINEvaluator(
            mpin=case["mpin"],
            dob_self=dob_self_val,
            dob_spouse=dob_spouse_val,
            anniversary=anniversary_val
        )
        result = evaluator.evaluate_strength()
        print(f"Test Case {i}: MPIN='{result['MPIN']}', Strength='{result['Strength']}' (Expected: '{case['expected_strength']}')")
        if result['Reasons']:
            print(f"  Reasons: {', '.join(result['Reasons'])}")
        print(f"  Comment: {case['comment']}\n")


if __name__ == "__main__":
    run_tests()