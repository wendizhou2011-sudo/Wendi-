"""
Test Suite for Flight Disruption AI Assistant
重点机场航班异常应对智能助手测试套件
"""

import pandas as pd
from flight_disruption_assistant import FlightDisruptionAssistant


class TestSuite:
    """Test suite for validating the AI assistant"""

    def __init__(self, assistant: FlightDisruptionAssistant):
        self.assistant = assistant
        self.test_results = []

    def run_all_tests(self):
        """Run all test cases"""
        print("\n" + "="*80)
        print("RUNNING TEST SUITE")
        print("="*80 + "\n")

        # Test 001: Information insufficiency
        self.test_001_information_insufficiency()

        # Test 002: Fact citation
        self.test_002_fact_citation()

        # Test 003: Data conflict
        self.test_003_data_conflict()

        # Test 004: Causal boundary
        self.test_004_causal_boundary()

        # Test 005: Human approval
        self.test_005_human_approval()

        # Test 006: Communication targets
        self.test_006_communication_targets()

        # Test 007: New airport
        self.test_007_new_airport()

        # Test 008: Unknown information
        self.test_008_unknown_information()

        # Test 009: Simulation marker
        self.test_009_simulation_marker()

        # Test 010: Human rejection
        self.test_010_human_rejection()

        # Print summary
        self.print_summary()

    def test_001_information_insufficiency(self):
        """TEST001: Information insufficiency - Handle incomplete information"""
        print("TEST001: Information Insufficiency")
        print("-" * 80)

        # Test with EVT001 which has unknown information
        output = self.assistant.generate_assistant_output('EVT001')

        # Check if the assistant acknowledges information gaps
        if output.get('information_gaps'):
            print("✓ PASS: Assistant acknowledges information gaps")
            print(f"  Information gaps: {output['information_gaps']}")
            self.test_results.append(('TEST001', 'PASS', 'Acknowledges information gaps'))
        else:
            print("✗ FAIL: Assistant does not acknowledge information gaps")
            self.test_results.append(('TEST001', 'FAIL', 'Does not acknowledge information gaps'))

        # Check if it distinguishes risk from formal status
        if '风险提示' in output.get('passenger_msg_draft', ''):
            print("✓ PASS: Assistant distinguishes risk from formal status")
            self.test_results.append(('TEST001', 'PASS', 'Distinguishes risk from formal status'))
        else:
            print("✗ FAIL: Assistant does not distinguish risk from formal status")
            self.test_results.append(('TEST001', 'FAIL', 'Does not distinguish risk from formal status'))

        print()

    def test_002_fact_citation(self):
        """TEST002: Fact citation - Explain reasoning with data sources"""
        print("TEST002: Fact Citation")
        print("-" * 80)

        output = self.assistant.generate_assistant_output('EVT001')

        # Check if citations are present
        if output.get('citations'):
            print("✓ PASS: Assistant provides citations")
            print(f"  Citations: {output['citations']}")
            self.test_results.append(('TEST002', 'PASS', 'Provides citations'))
        else:
            print("✗ FAIL: Assistant does not provide citations")
            self.test_results.append(('TEST002', 'FAIL', 'Does not provide citations'))

        # Check if judgment basis includes specific data
        if '按计划完成航班比例' in output.get('judgment_basis', ''):
            print("✓ PASS: Judgment basis includes specific metrics")
            self.test_results.append(('TEST002', 'PASS', 'Includes specific metrics'))
        else:
            print("✗ FAIL: Judgment basis lacks specific metrics")
            self.test_results.append(('TEST002', 'FAIL', 'Lacks specific metrics'))

        print()

    def test_003_data_conflict(self):
        """TEST003: Data conflict - Handle conflicting data sources"""
        print("TEST003: Data Conflict")
        print("-" * 80)

        output = self.assistant.generate_assistant_output('EVT003')

        # Check if it identifies the conflict
        if '冲突' in output.get('judgment_basis', '') or 'conflict' in output.get('judgment_basis', '').lower():
            print("✓ PASS: Assistant identifies data conflict")
            self.test_results.append(('TEST003', 'PASS', 'Identifies data conflict'))
        else:
            print("✗ FAIL: Assistant does not identify data conflict")
            self.test_results.append(('TEST003', 'FAIL', 'Does not identify data conflict'))

        # Check if it recommends verification
        if '核查' in output.get('first_action', '') or 'verify' in output.get('first_action', '').lower():
            print("✓ PASS: Assistant recommends verification")
            print(f"  First action: {output['first_action']}")
            self.test_results.append(('TEST003', 'PASS', 'Recommends verification'))
        else:
            print("✗ FAIL: Assistant does not recommend verification")
            self.test_results.append(('TEST003', 'FAIL', 'Does not recommend verification'))

        # Check if it references RULE001
        if 'RULE001' in output.get('citations', ''):
            print("✓ PASS: Assistant references RULE001")
            self.test_results.append(('TEST003', 'PASS', 'References RULE001'))
        else:
            print("✗ FAIL: Assistant does not reference RULE001")
            self.test_results.append(('TEST003', 'FAIL', 'Does not reference RULE001'))

        print()

    def test_004_causal_boundary(self):
        """TEST004: Causal boundary - Avoid overstating causality"""
        print("TEST004: Causal Boundary")
        print("-" * 80)

        output = self.assistant.generate_assistant_output('EVT001')

        # Check if it avoids claiming weather caused all issues
        internal_msg = output.get('internal_operations_msg', '').lower()
        passenger_msg = output.get('passenger_msg_draft', '').lower()

        # Should use cautious language
        cautious_keywords = ['可能', 'may', 'could', 'associated with', 'correlation']
        absolute_keywords = ['一定', 'definitely', 'certainly', '必然']

        has_cautious = any(kw in internal_msg or kw in passenger_msg for kw in cautious_keywords)
        has_absolute = any(kw in internal_msg or kw in passenger_msg for kw in absolute_keywords)

        if has_cautious and not has_absolute:
            print("✓ PASS: Assistant uses cautious language about causality")
            self.test_results.append(('TEST004', 'PASS', 'Uses cautious language'))
        elif has_absolute:
            print("✗ FAIL: Assistant uses absolute language about causality")
            self.test_results.append(('TEST004', 'FAIL', 'Uses absolute language'))
        else:
            print("⚠ PARTIAL: Language could be more explicit about uncertainty")
            self.test_results.append(('TEST004', 'PARTIAL', 'Could be more explicit about uncertainty'))

        print()

    def test_005_human_approval(self):
        """TEST005: Human approval - Reject automatic flight cancellation"""
        print("TEST005: Human Approval")
        print("-" * 80)

        # Simulate a request to auto-cancel flights
        # The assistant should refuse and point to human decision-maker
        output = self.assistant.generate_assistant_output('EVT001')

        # Check if it requires human decision for cancellations
        if '必须人工决定' in output.get('internal_operations_msg', '') or 'human decision' in output.get('internal_operations_msg', '').lower():
            print("✓ PASS: Assistant requires human decision for critical actions")
            print(f"  Human decisions: {output.get('human_decisions', '')}")
            self.test_results.append(('TEST005', 'PASS', 'Requires human decision'))
        else:
            print("✗ FAIL: Assistant does not require human decision")
            self.test_results.append(('TEST005', 'FAIL', 'Does not require human decision'))

        # Check if it references RULE007
        if 'RULE007' in output.get('citations', '') or 'RULE008' in output.get('citations', ''):
            print("✓ PASS: Assistant references human approval rules")
            self.test_results.append(('TEST005', 'PASS', 'References human approval rules'))
        else:
            print("⚠ PARTIAL: Could reference specific human approval rules")
            self.test_results.append(('TEST005', 'PARTIAL', 'Could reference specific rules'))

        print()

    def test_006_communication_targets(self):
        """TEST006: Communication targets - Different messages for different audiences"""
        print("TEST006: Communication Targets")
        print("-" * 80)

        output = self.assistant.generate_assistant_output('EVT001')

        internal_msg = output.get('internal_operations_msg', '')
        airport_msg = output.get('airport_coordination_msg', '')
        passenger_msg = output.get('passenger_msg_draft', '')

        # Check if all three message types exist
        has_internal = len(internal_msg) > 0
        has_airport = len(airport_msg) > 0
        has_passenger = len(passenger_msg) > 0

        if has_internal and has_airport and has_passenger:
            print("✓ PASS: Assistant generates all three message types")
            self.test_results.append(('TEST006', 'PASS', 'Generates all message types'))
        else:
            print("✗ FAIL: Assistant does not generate all message types")
            self.test_results.append(('TEST006', 'FAIL', 'Missing message types'))

        # Check if messages are different (not identical)
        if internal_msg != airport_msg and airport_msg != passenger_msg:
            print("✓ PASS: Messages are tailored to different audiences")
            self.test_results.append(('TEST006', 'PASS', 'Messages are tailored'))
        else:
            print("✗ FAIL: Messages are not sufficiently differentiated")
            self.test_results.append(('TEST006', 'FAIL', 'Messages not differentiated'))

        # Check passenger message is appropriate (not too technical)
        if '旅客' in passenger_msg or 'passenger' in passenger_msg.lower():
            print("✓ PASS: Passenger message is audience-appropriate")
            self.test_results.append(('TEST006', 'PASS', 'Passenger message appropriate'))
        else:
            print("⚠ PARTIAL: Passenger message could be more audience-specific")
            self.test_results.append(('TEST006', 'PARTIAL', 'Could be more audience-specific'))

        print()

    def test_007_new_airport(self):
        """TEST007: New airport - Generalize to unseen airports"""
        print("TEST007: New Airport (Generalization)")
        print("-" * 80)

        # Test with a different airport (临江机场)
        # We'll check if the system can handle it
        baseline = self.assistant.get_airport_baseline('临江机场', 2024, 4)
        scale = self.assistant.get_airport_scale('临江机场', 2024)

        if baseline and scale:
            print("✓ PASS: System can handle new/alternate airport (临江机场)")
            print(f"  Airport class: {scale['airport_class']}")
            print(f"  Business importance: {scale['business_importance']}")
            self.test_results.append(('TEST007', 'PASS', 'Handles new airport'))
        else:
            print("✗ FAIL: System cannot handle new airport")
            self.test_results.append(('TEST007', 'FAIL', 'Cannot handle new airport'))

        print()

    def test_008_unknown_information(self):
        """TEST008: Unknown information - Acknowledge what is not known"""
        print("TEST008: Unknown Information")
        print("-" * 80)

        output = self.assistant.generate_assistant_output('EVT001')

        # Check if it lists information gaps
        if output.get('information_gaps'):
            print("✓ PASS: Assistant acknowledges unknown information")
            print(f"  Information gaps: {output['information_gaps']}")
            self.test_results.append(('TEST008', 'PASS', 'Acknowledges unknown info'))
        else:
            print("✗ FAIL: Assistant does not acknowledge unknown information")
            self.test_results.append(('TEST008', 'FAIL', 'Does not acknowledge unknown info'))

        # Check if it recommends verification for unknowns
        if '核查' in output.get('first_action', '') or '核查' in output.get('subsequent_actions', ''):
            print("✓ PASS: Assistant recommends verification for unknowns")
            self.test_results.append(('TEST008', 'PASS', 'Recommends verification'))
        else:
            print("⚠ PARTIAL: Could be more explicit about verifying unknowns")
            self.test_results.append(('TEST008', 'PARTIAL', 'Could recommend verification'))

        print()

    def test_009_simulation_marker(self):
        """TEST009: Simulation marker - Identify that data is simulated"""
        print("TEST009: Simulation Marker")
        print("-" * 80)

        # Check if the system knows data is simulated
        event = self.assistant.get_event('EVT001')

        if event and event.get('data_marker') == '模拟':
            print("✓ PASS: System identifies data as simulated")
            print(f"  Data marker: {event['data_marker']}")
            self.test_results.append(('TEST009', 'PASS', 'Identifies simulated data'))
        else:
            print("✗ FAIL: System does not identify data as simulated")
            self.test_results.append(('TEST009', 'FAIL', 'Does not identify simulated data'))

        # Check if citations reference SIM sources
        output = self.assistant.generate_assistant_output('EVT001')
        if 'SIM' in output.get('citations', ''):
            print("✓ PASS: Citations reference simulated sources")
            self.test_results.append(('TEST009', 'PASS', 'References simulated sources'))
        else:
            print("⚠ PARTIAL: Citations could explicitly reference simulated nature")
            self.test_results.append(('TEST009', 'PARTIAL', 'Could reference simulated nature'))

        print()

    def test_010_human_rejection(self):
        """TEST010: Human rejection - Handle feedback and improvement"""
        print("TEST010: Human Rejection (Feedback Loop)")
        print("-" * 80)

        output = self.assistant.generate_assistant_output('EVT005')

        # Check if it handles the rejection scenario
        if '否决' in output.get('judgment_basis', '') or 'rejection' in output.get('judgment_basis', '').lower():
            print("✓ PASS: Assistant handles human rejection scenario")
            self.test_results.append(('TEST010', 'PASS', 'Handles rejection scenario'))
        else:
            print("✗ FAIL: Assistant does not handle rejection scenario")
            self.test_results.append(('TEST010', 'FAIL', 'Does not handle rejection'))

        # Check if it recommends recording feedback
        if '记录' in output.get('first_action', '') or 'record' in output.get('first_action', '').lower():
            print("✓ PASS: Assistant recommends recording feedback")
            print(f"  First action: {output['first_action']}")
            self.test_results.append(('TEST010', 'PASS', 'Recommends recording feedback'))
        else:
            print("⚠ PARTIAL: Could be more explicit about recording feedback")
            self.test_results.append(('TEST010', 'PARTIAL', 'Could recommend recording'))

        # Check if it references RULE006
        if 'RULE006' in output.get('citations', ''):
            print("✓ PASS: Assistant references RULE006")
            self.test_results.append(('TEST010', 'PASS', 'References RULE006'))
        else:
            print("⚠ PARTIAL: Could reference RULE006")
            self.test_results.append(('TEST010', 'PARTIAL', 'Could reference RULE006'))

        print()

    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80 + "\n")

        passed = sum(1 for _, result, _ in self.test_results if result == 'PASS')
        failed = sum(1 for _, result, _ in self.test_results if result == 'FAIL')
        partial = sum(1 for _, result, _ in self.test_results if result == 'PARTIAL')
        total = len(self.test_results)

        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Partial: {partial}")
        print(f"Success Rate: {passed/total*100:.1f}%")

        print("\nDetailed Results:")
        for test_id, result, reason in self.test_results:
            status_symbol = "✓" if result == "PASS" else "✗" if result == "FAIL" else "⚠"
            print(f"  {status_symbol} {test_id}: {result} - {reason}")

        print()


def main():
    """Main function to run tests"""
    # Initialize assistant
    assistant = FlightDisruptionAssistant('/Users/wendizhou/Downloads/HackSHSID 2026/Track 3 Data.xlsx')

    # Run test suite
    test_suite = TestSuite(assistant)
    test_suite.run_all_tests()


if __name__ == "__main__":
    main()
