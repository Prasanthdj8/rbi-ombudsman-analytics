"""
generate_synthetic_complaints.py

Generates SYNTHETIC, author-written complaint-style text samples mapped to
RBI's real, published Ombudsman complaint categories (Loans and Advances,
Credit Cards, ATM/Debit Cards, Mobile/Electronic Banking, Deposit Accounts,
Pension Related).

IMPORTANT: This data is entirely synthetic. RBI does not publish individual
complaint narratives. This script exists to produce realistic-looking training
text so the classifier has something to learn from, demonstrating the NLP
pipeline a Young Professional role in this department would build. It is not,
and is not presented as, real complainant data. See ../data/SOURCES.md and
README.md for full disclosure.
"""

import csv
import random

random.seed(42)

CATEGORIES = {
    "Loans and Advances": [
        "My home loan EMI was deducted twice in the same month and the bank has not refunded the extra amount despite repeated follow up.",
        "I applied for a personal loan foreclosure and the bank is charging a penalty that was never mentioned in my loan agreement.",
        "The interest rate on my floating rate loan was increased without any prior notice being sent to me.",
        "My loan account shows a default even though I have paid every installment on time for the last two years.",
        "The bank sanctioned my car loan but is delaying disbursement for over six weeks without explanation.",
        "I was charged a processing fee on my loan that is double what was quoted to me at the time of application.",
        "My request to convert my loan from floating to fixed rate has been ignored for three months now.",
        "The bank has not issued a no objection certificate even though I closed my loan account five months ago.",
        "I am being asked to pay prepayment charges on my loan despite RBI guidelines stating otherwise for floating rate loans.",
        "My loan top up application was rejected without any written reason being provided to me.",
    ],
    "Credit Cards": [
        "I am being billed an annual fee on my credit card that was supposed to be lifetime free as per the original offer.",
        "A transaction I never made appeared on my credit card statement and the bank is refusing to investigate it.",
        "My credit card reward points expired without any prior communication from the bank.",
        "I was charged a late payment fee even though I paid my credit card bill one day before the due date.",
        "The bank increased my credit card limit without my consent and now wants to charge interest on the new limit.",
        "My credit card application was rejected and the bank will not tell me the specific reason for rejection.",
        "I requested closure of my credit card four months ago but I am still being charged the annual renewal fee.",
        "There is a billing dispute on my credit card statement that the bank has not resolved after sixty days.",
        "I was charged GST twice on the same credit card transaction in one billing cycle.",
        "My credit card was blocked without notice while I was traveling and customer care could not explain why.",
    ],
    "ATM/Debit Cards": [
        "Cash was deducted from my account at the ATM but the machine did not dispense any money.",
        "My debit card was used for a transaction in another city while the card was in my possession the entire time.",
        "The bank is charging me an ATM usage fee even though I have not exceeded my free transaction limit for the month.",
        "I reported a failed ATM transaction over a month ago and the amount has still not been reversed to my account.",
        "My debit card stopped working without any notice and the branch could not tell me why it was blocked.",
        "I was charged for a duplicate debit card that I never requested or received.",
        "The ATM swallowed my card during a transaction and the branch has not returned it after two weeks.",
        "My debit card PIN reset request has been pending for over three weeks with no update from the bank.",
    ],
    "Mobile/Electronic Banking": [
        "An unauthorized UPI transaction was made from my account and the bank has not blocked the linked merchant.",
        "My mobile banking app shows a failed transaction but the amount was still deducted from my account.",
        "I am unable to log into net banking for two weeks now and customer support has not resolved the issue.",
        "A fund transfer through the mobile app went to the wrong account due to an app error and the bank refuses to help recover it.",
        "My OTP for a transaction I did not initiate was used to debit money from my savings account.",
        "The mobile banking app charged me a service fee that was never disclosed in the terms of use.",
        "I am facing repeated failed login attempts being flagged on my account despite using the correct credentials.",
        "My NEFT transfer initiated through net banking has been stuck in processing for five days.",
    ],
    "Deposit Accounts": [
        "My fixed deposit was auto renewed at a lower interest rate than what was originally communicated to me.",
        "The bank closed my savings account for inactivity without sending any prior written notice.",
        "I am unable to withdraw my matured fixed deposit because the branch says my KYC documents need updating, which I already submitted.",
        "My joint account was frozen after one holder passed away and the bank is not processing the required transmission paperwork.",
        "The bank deducted a minimum balance penalty from my account despite my maintaining the required average balance.",
        "My recurring deposit installment was not credited correctly and the maturity amount shown is incorrect.",
    ],
    "Pension Related": [
        "My pension payment was delayed by over a month with no explanation from the bank handling my pension account.",
        "The bank has not updated my pension account after my annual life certificate submission, and payments have stopped.",
        "There is a discrepancy in my pension amount compared to what was sanctioned by my employer, and the branch is not resolving it.",
        "My family pension claim after my spouse's death has been pending at the branch for over four months.",
    ],
}


def generate_dataset(output_path: str, samples_per_category: int = 40):
    rows = []
    for category, seeds in CATEGORIES.items():
        # Use the seed sentences directly, then create light variations
        # by combining seeds with neutral framing phrases. This keeps
        # everything readable and avoids any external data dependency.
        openers = ["", "I want to report that ", "I am writing to complain that ", "To whom it may concern, "]
        closers = ["", " Please resolve this at the earliest.", " I have already raised this with the branch.", " Kindly look into this matter."]

        count = 0
        while count < samples_per_category:
            seed = random.choice(seeds)
            opener = random.choice(openers)
            closer = random.choice(closers)
            text = f"{opener}{seed[0].lower() + seed[1:] if opener else seed}{closer}"
            rows.append({"text": text, "category": category})
            count += 1

    random.shuffle(rows)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "category"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} synthetic complaint samples across {len(CATEGORIES)} categories.")
    print(f"Saved to {output_path}")


if __name__ == "__main__":
    generate_dataset("synthetic_complaints.csv", samples_per_category=40)
