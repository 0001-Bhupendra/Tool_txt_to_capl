"""
CAPL Test Code Generator for Vector vTESTstudio
Converts extracted test case JSON data into CAPL test module code.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


class CAPLCodeGenerator:
    """Generate CAPL test code from extracted test case data."""
    
    def __init__(self):
        self.indentation = "  "  # 2 spaces for CAPL indentation
    
    def indent(self, level: int) -> str:
        """Return indentation string for given level."""
        return self.indentation * level
    
    def generate_header(self, metadata: Dict[str, str]) -> str:
        """Generate CAPL file header with test case metadata."""
        lines = [
            "///////////////////////////////////////////////////////////////////////////////",
            "// CAPL Test Module",
            f"// Test Case ID: {metadata.get('id', 'Unknown')}",
            f"// Test Case: {metadata.get('title', 'Unknown')}",
            f"// Component: {metadata.get('component', 'Unknown')}",
            f"// Generated automatically from PDF test case",
            "//",
            "// This module implements automated test execution for the above test case",
            "///////////////////////////////////////////////////////////////////////////////",
            "",
            "// Include necessary headers and libraries",
            "#include \"stdlib.can\"",
            "",
        ]
        return "\n".join(lines)
    
    def parse_signal_name(self, signal: str) -> str:
        """Extract clean signal name from various formats."""
        # Remove 'Stimulate' keyword if present
        signal = signal.replace('Stimulate', '').strip()
        # Extract base signal name
        return signal.split('(')[0].strip()
    
    def parse_signal_value(self, value_str: str) -> str:
        """Parse signal value from various formats."""
        # Handle "value" in parentheses format: "ON(4)" -> "4"
        if '(' in value_str and ')' in value_str:
            return value_str.split('(')[1].rstrip(')')
        # Handle "0->1" format: return target value "1"
        if '->' in value_str:
            return value_str.split('->')[-1].strip()
        # Handle plain values
        return value_str.strip().strip('"\'')
    
    def generate_pre_condition_section(self, pre_conditions: Dict[str, str]) -> str:
        """Generate pre-condition setup code."""
        if not pre_conditions:
            return ""
        
        lines = [
            "///////////////////////////////////////////////////////////////////////////////",
            "// Pre-Condition Setup",
            "///////////////////////////////////////////////////////////////////////////////",
            "",
            "void setup_pre_conditions()",
            "{",
        ]
        
        for var, value in pre_conditions.items():
            # Clean variable name
            var_clean = var.replace('si_sys_', '').replace('Stimulate ', '')
            value_clean = self.parse_signal_value(value)
            
            if 'si_sys_' in var:
                # Input signal setup
                lines.append(f"{self.indent(1)}write(\"{var_clean}\", {value_clean});")
            else:
                # Stimulation command
                lines.append(f"{self.indent(1)}// Stimulate {var_clean} to {value_clean}")
                lines.append(f"{self.indent(1)}vtsStimulateSignal(\"{var_clean}\", {value_clean});")
        
        lines.extend([
            "",
            "  // Allow system to settle",
            "  wait(100); // ms",
            "}",
            "",
        ])
        
        return "\n".join(lines)
    
    def generate_post_condition_section(self, post_conditions: Dict[str, str]) -> str:
        """Generate post-condition cleanup code."""
        if not post_conditions:
            return ""
        
        lines = [
            "///////////////////////////////////////////////////////////////////////////////",
            "// Post-Condition Cleanup",
            "///////////////////////////////////////////////////////////////////////////////",
            "",
            "void cleanup_post_conditions()",
            "{",
        ]
        
        for var, value in post_conditions.items():
            var_clean = var.replace('si_sys_', '').replace('Stimulate ', '')
            value_clean = self.parse_signal_value(value)
            
            if 'si_sys_' in var:
                lines.append(f"{self.indent(1)}write(\"{var_clean}\", {value_clean});")
            else:
                lines.append(f"{self.indent(1)}vtsStimulateSignal(\"{var_clean}\", {value_clean});")
        
        lines.append(f"{self.indent(1)}wait(100); // ms")
        lines.extend([
            "}",
            "",
        ])
        
        return "\n".join(lines)
    
    def generate_stimulation_section(self, stimulations: List[Dict[str, Any]]) -> str:
        """Generate stimulation test steps."""
        lines = [
            "///////////////////////////////////////////////////////////////////////////////",
            "// Test Stimulation Steps",
            "///////////////////////////////////////////////////////////////////////////////",
            "",
        ]
        
        for stim in stimulations:
            stim_num = stim.get('number', '0')
            stim_title = stim.get('title', 'Unknown')
            actions = stim.get('actions', {})
            expected = stim.get('expected_results', {})
            
            # Create function name
            func_name = f"stimulation_step_{stim_num}"
            
            lines.extend([
                f"// Stimulation-{stim_num}: {stim_title}",
                f"void {func_name}()",
                "{",
                f"{self.indent(1)}write(\"Starting stimulation {stim_num}...\");",
            ])
            
            # Generate stimulation actions
            for action, value in actions.items():
                if action == 'fault_type':
                    continue  # Handle with fault_target
                elif action == 'fault_target':
                    fault_type = actions.get('fault_type', 'SCG')
                    lines.append(f"{self.indent(1)}// Create {fault_type} fault on {value}")
                    lines.append(f"{self.indent(1)}vtsCreateFault(\"{value}\", \"{fault_type}\");")
                elif action == 'remove_fault':
                    lines.append(f"{self.indent(1)}// Remove injected fault")
                    lines.append(f"{self.indent(1)}vtsRemoveFault(\"{actions.get('fault_target', 'B21')}\");")
                elif 'Proxy_write' in action:
                    signal_name = action.replace('Proxy_write_', '')
                    signal_value = self.parse_signal_value(str(value))
                    lines.append(f"{self.indent(1)}write(\"{signal_name}\", {signal_value});")
                elif 'Stimulate' in action:
                    signal_name = self.parse_signal_name(action)
                    signal_value = self.parse_signal_value(str(value))
                    lines.append(f"{self.indent(1)}vtsStimulateSignal(\"{signal_name}\", {signal_value});")
                else:
                    signal_value = self.parse_signal_value(str(value))
                    lines.append(f"{self.indent(1)}write(\"{action}\", {signal_value});")
            
            lines.append(f"{self.indent(1)}wait(100); // Allow system to respond")
            
            # Generate expected result validations
            if expected:
                lines.append(f"{self.indent(1)}// Expected Results")
                
                if expected.get('NO_DTC'):
                    lines.append(f"{self.indent(1)}if (!checkNoActiveDTC())")
                    lines.append(f"{self.indent(1)}{{")
                    lines.append(f"{self.indent(2)}setResult(FAIL, \"Expected NO DTC but found active DTC\");")
                    lines.append(f"{self.indent(1)}}}")
                
                if 'DTC_active' in expected:
                    dtc_list = expected['DTC_active']
                    if isinstance(dtc_list, list):
                        for dtc in dtc_list:
                            lines.append(f"{self.indent(1)}if (!checkActiveDTC(\"{dtc}\"))")
                            lines.append(f"{self.indent(1)}{{")
                            lines.append(f"{self.indent(2)}setResult(FAIL, \"Expected DTC {dtc} but not found\");")
                            lines.append(f"{self.indent(1)}}}")
                    else:
                        lines.append(f"{self.indent(1)}if (!checkActiveDTC(\"{dtc_list}\"))")
                        lines.append(f"{self.indent(1)}{{")
                        lines.append(f"{self.indent(2)}setResult(FAIL, \"Expected DTC {dtc_list} but not found\");")
                        lines.append(f"{self.indent(1)}}}")
                
                # Check signal values
                for signal, value in expected.items():
                    if signal not in ('DTC_active', 'NO_DTC') and not isinstance(value, (bool, list)):
                        if '->' in str(value):
                            # Extract expected value from "0->1" format
                            expected_value = str(value).split('->')[-1].strip()
                            lines.append(f"{self.indent(1)}if (!checkSignalValue(\"{signal}\", {expected_value}))")
                            lines.append(f"{self.indent(1)}{{")
                            lines.append(f"{self.indent(2)}setResult(FAIL, \"{signal} did not reach expected value {expected_value}\");")
                            lines.append(f"{self.indent(1)}}}")
            
            lines.extend([
                "}",
                "",
            ])
        
        return "\n".join(lines)
    
    def generate_helper_functions(self) -> str:
        """Generate helper functions for common test operations."""
        lines = [
            "///////////////////////////////////////////////////////////////////////////////",
            "// Helper Functions",
            "///////////////////////////////////////////////////////////////////////////////",
            "",
            "// Check if a specific DTC is active",
            "int checkActiveDTC(char dtcCode[])",
            "{",
            "  // TODO: Implement DTC checking logic using vTESTstudio API",
            "  // This should query the active DTCs and check if 'dtcCode' exists",
            "  return 1;  // Placeholder",
            "}",
            "",
            "// Check if no DTCs are active",
            "int checkNoActiveDTC()",
            "{",
            "  // TODO: Implement no DTC checking logic",
            "  // This should verify that the DTC list is empty",
            "  return 1;  // Placeholder",
            "}",
            "",
            "// Check if a signal has a specific value",
            "int checkSignalValue(char signalName[], long expectedValue)",
            "{",
            "  long actualValue;",
            "  read(signalName, actualValue);",
            "  if (actualValue == expectedValue)",
            "    return 1;",
            "  else",
            "    return 0;",
            "}",
            "",
            "// Set test result",
            "void setResult(int result, char message[])",
            "{",
            "  // TODO: Implement result logging",
            "  if (result == PASS)",
            "    write(\"[PASS] \" + message);",
            "  else",
            "    write(\"[FAIL] \" + message);",
            "}",
            "",
            "// Create a fault on a node",
            "void vtsCreateFault(char nodeName[], char faultType[])",
            "{",
            "  // TODO: Implement fault injection using vTESTstudio Fault Insertion API",
            "  write(\"Creating \" + faultType + \" fault on \" + nodeName);",
            "}",
            "",
            "// Remove a fault",
            "void vtsRemoveFault(char nodeName[])",
            "{",
            "  // TODO: Implement fault removal using vTESTstudio API",
            "  write(\"Removing fault from \" + nodeName);",
            "}",
            "",
            "// Stimulate a signal to a specific value",
            "void vtsStimulateSignal(char signalName[], long value)",
            "{",
            "  // TODO: Implement signal stimulation using vTESTstudio API",
            "  write(\"Stimulating \" + signalName + \" to \" + value);",
            "  // Example: write(signalName, value);",
            "}",
            "",
            "// Define result codes",
            "#define PASS 1",
            "#define FAIL 0",
            "",
        ]
        
        return "\n".join(lines)
    
    def generate_main_test(self, test_id: str) -> str:
        """Generate main test execution function."""
        lines = [
            "///////////////////////////////////////////////////////////////////////////////",
            "// Main Test Execution",
            "///////////////////////////////////////////////////////////////////////////////",
            "",
            f"test {test_id}()",
            "{",
            "  dword startTime;",
            "  int testResult = PASS;",
            "",
            "  startTime = GetTickCount();",
            "  write(\"\\n========== Starting Test Case ==========\");",
            "",
            "  // Setup pre-conditions",
            "  setup_pre_conditions();",
            "",
            "  // Execute stimulation steps",
            "  stimulation_step_1();",
            "  stimulation_step_2();",
            "  stimulation_step_3();",
            "  stimulation_step_4();",
            "  stimulation_step_5();",
            "",
            "  // Cleanup post-conditions",
            "  cleanup_post_conditions();",
            "",
            "  // Report final result",
            "  if (testResult == PASS)",
            "    write(\"[RESULT] Test PASSED\");",
            "  else",
            "    write(\"[RESULT] Test FAILED\");",
            "",
            "  write(\"Execution time: \" + (GetTickCount() - startTime) + \" ms\");",
            "  write(\"========== Test Complete ==========\");",
            "}",
            "",
        ]
        
        return "\n".join(lines)
    
    def generate_full_capl_code(self, test_data: Dict[str, Any]) -> str:
        """Generate complete CAPL test module code."""
        metadata = test_data.get('metadata', {})
        pre_conditions = test_data.get('pre_condition', {})
        stimulations = test_data.get('stimulations', [])
        post_conditions = test_data.get('post_condition', {})
        
        code_parts = [
            self.generate_header(metadata),
            self.generate_pre_condition_section(pre_conditions),
            self.generate_stimulation_section(stimulations),
            self.generate_post_condition_section(post_conditions),
            self.generate_helper_functions(),
            self.generate_main_test(metadata.get('id', 'test_case')),
        ]
        
        return "\n".join(code_parts)
    
    def save_capl_file(self, capl_code: str, output_path: str) -> None:
        """Save generated CAPL code to file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(capl_code)
        
        print(f"CAPL code saved to: {output_path}")


def main():
    """Main function to generate CAPL code from extracted JSON."""
    if len(sys.argv) < 2:
        print("Usage: python capl_code_generator.py <json_file> [output_file]")
        print("\nExample:")
        print("  python capl_code_generator.py TC_7778_extracted.json")
        print("  python capl_code_generator.py TC_7778_extracted.json my_test.can")
        sys.exit(1)
    
    json_file = sys.argv[1]
    json_path = Path(json_file)
    
    # Validate JSON file exists
    if not json_path.exists():
        print(f"Error: JSON file not found: {json_file}")
        sys.exit(1)
    
    # Load JSON data
    print(f"Loading test case data from: {json_file}")
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            test_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        sys.exit(1)
    
    # Determine output file path
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        output_file = str(json_path.parent / f"{json_path.stem}_generated.can")
    
    # Generate CAPL code
    print("Generating CAPL code...")
    generator = CAPLCodeGenerator()
    
    try:
        capl_code = generator.generate_full_capl_code(test_data)
        generator.save_capl_file(capl_code, output_file)
        
        print("\n" + "=" * 70)
        print("CAPL CODE GENERATION COMPLETE")
        print("=" * 70)
        print(f"Generated {len(capl_code.split(chr(10)))} lines of CAPL code")
        print("\nNOTE: The generated code contains placeholder helper functions.")
        print("You must implement the following for your specific environment:")
        print("  - vtsCreateFault(): Fault injection logic")
        print("  - vtsRemoveFault(): Fault removal logic")
        print("  - vtsStimulateSignal(): Signal stimulation logic")
        print("  - checkActiveDTC(): DTC checking logic")
        print("  - checkNoActiveDTC(): No DTC verification logic")
        
    except Exception as e:
        print(f"Error generating CAPL code: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
