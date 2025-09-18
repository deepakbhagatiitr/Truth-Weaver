#!/usr/bin/env python3
"""
Smart AI Interviewer Decision Flow Generator
Creates interactive flowcharts for the AI interviewer decision-making process.

Usage: python ai_interviewer_flowchart.py
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

def create_ai_interviewer_flowchart():
    """Create a comprehensive flowchart of the AI interviewer decision process."""
    
    # Create figure and axis
    fig, ax = plt.subplots(1, 1, figsize=(16, 20))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 25)
    ax.axis('off')
    
    # Color scheme
    colors = {
        'start': '#4CAF50',      # Green
        'decision': '#2196F3',   # Blue  
        'process': '#FF9800',    # Orange
        'action': '#9C27B0',     # Purple
        'alert': '#F44336',      # Red
        'end': '#607D8B'         # Blue Grey
    }
    
    # Helper function to create boxes
    def create_box(x, y, width, height, text, color_key, text_size=10):
        box = FancyBboxPatch(
            (x-width/2, y-height/2), width, height,
            boxstyle="round,pad=0.1",
            facecolor=colors[color_key],
            edgecolor='black',
            linewidth=1.5,
            alpha=0.8
        )
        ax.add_patch(box)
        
        # Add text with word wrapping
        ax.text(x, y, text, ha='center', va='center', 
                fontsize=text_size, fontweight='bold', 
                color='white', wrap=True)
    
    # Helper function to create arrows
    def create_arrow(x1, y1, x2, y2, text=''):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=2, color='black'))
        if text:
            mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mid_x + 0.2, mid_y, text, fontsize=8, 
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # Title
    ax.text(5, 24, '🧠 SMART AI INTERVIEWER DECISION FRAMEWORK', 
            ha='center', va='center', fontsize=18, fontweight='bold')
    
    # Flow components
    # 1. Start
    create_box(5, 22.5, 2.5, 0.8, '🎤 Interview Start', 'start')
    
    # 2. Audio Input Detection
    create_box(5, 21, 2.5, 0.8, '🔊 Audio Input\nDetected?', 'decision')
    create_arrow(5, 22.1, 5, 21.4)
    
    # 3. Transcription
    create_box(5, 19.5, 2.5, 0.8, '📝 Real-time\nTranscription', 'process')
    create_arrow(5, 20.6, 5, 19.9, 'Yes')
    
    # Wait loop
    create_box(8, 21, 1.5, 0.6, '⏳ Wait &\nListen', 'action')
    create_arrow(6.25, 21, 7.25, 21, 'No')
    create_arrow(8, 20.7, 8, 21.4)
    create_arrow(7.25, 21.4, 6.25, 21.4)
    
    # 4. Analysis Engine
    create_box(5, 18, 2.5, 0.8, '🧠 Live Analysis\nEngine', 'process')
    create_arrow(5, 19.1, 5, 18.4)
    
    # 5. Response Quality Check
    create_box(5, 16.5, 2.5, 0.8, '🎯 Response Quality\nCheck', 'decision')
    create_arrow(5, 17.6, 5, 16.9)
    
    # 6. Quality Assessment Branches
    # Complete & Clear
    create_box(1.5, 15, 2, 0.6, '✅ Complete\n& Clear', 'action')
    create_arrow(3.75, 16.5, 2.5, 15.3)
    
    # Incomplete
    create_box(4, 15, 2, 0.6, '❓ Incomplete', 'action')  
    create_arrow(4.5, 16.1, 4.2, 15.4)
    
    # Evasive
    create_box(6, 15, 2, 0.6, '🎯 Evasive', 'alert')
    create_arrow(5.5, 16.1, 5.8, 15.4)
    
    # Contradictory
    create_box(8.5, 15, 2, 0.6, '🔍 Contradictory', 'alert')
    create_arrow(6.25, 16.5, 7.5, 15.3)
    
    # 7. Follow-up Actions
    create_box(1.5, 13.5, 2, 0.6, '📝 Store\nResponse', 'process')
    create_arrow(1.5, 14.7, 1.5, 13.8)
    
    create_box(4, 13.5, 2, 0.6, '💬 "Could you\nelaborate?"', 'action')
    create_arrow(4, 14.7, 4, 13.8)
    
    create_box(6, 13.5, 2, 0.6, '🔎 "Be more\nspecific"', 'action')
    create_arrow(6, 14.7, 6, 13.8)
    
    create_box(8.5, 13.5, 2, 0.6, '⚠️ "Earlier you\nsaid..."', 'alert')
    create_arrow(8.5, 14.7, 8.5, 13.8)
    
    # 8. Contradiction Analysis
    create_box(5, 12, 3, 0.8, '🚨 Contradiction Analysis\n& Severity Assessment', 'process')
    
    # Arrows to contradiction analysis
    create_arrow(1.5, 13.2, 3.5, 12.4)
    create_arrow(4, 13.2, 4.5, 12.4)
    create_arrow(6, 13.2, 5.5, 12.4)
    create_arrow(8.5, 13.2, 6.5, 12.4)
    
    # 9. Severity Assessment
    create_box(2, 10.5, 1.8, 0.6, '🔥 High\nSeverity', 'alert')
    create_box(5, 10.5, 1.8, 0.6, '📌 Medium\nSeverity', 'action')
    create_box(8, 10.5, 1.8, 0.6, '👀 Low\nSeverity', 'process')
    
    create_arrow(4, 11.6, 2.8, 10.8)
    create_arrow(5, 11.6, 5, 10.8)
    create_arrow(6, 11.6, 7.2, 10.8)
    
    # 10. Response Actions
    create_box(2, 9, 1.8, 0.6, '💬 Immediate\nChallenge', 'alert')
    create_box(5, 9, 1.8, 0.6, '📋 Note for\nLater', 'action')
    create_box(8, 9, 1.8, 0.6, '➡️ Continue\nMonitoring', 'process')
    
    create_arrow(2, 10.2, 2, 9.3)
    create_arrow(5, 10.2, 5, 9.3)
    create_arrow(8, 10.2, 8, 9.3)
    
    # 11. Coverage Check
    create_box(5, 7.5, 2.5, 0.8, '📊 Coverage\nComplete?', 'decision')
    
    # Arrows to coverage check
    create_arrow(2, 8.7, 4, 7.9)
    create_arrow(5, 8.7, 5, 7.9)
    create_arrow(8, 8.7, 6, 7.9)
    
    # 12. Final branches
    create_box(2.5, 6, 2, 0.6, '📈 Generate\nFinal Report', 'end')
    create_box(7.5, 6, 2, 0.6, '🎲 Dynamic Question\nGeneration', 'action')
    
    create_arrow(4.2, 7.2, 3.3, 6.4, 'Yes')
    create_arrow(5.8, 7.2, 6.7, 6.4, 'No')
    
    # 13. Loop back
    create_arrow(7.5, 6.3, 7.5, 18)
    create_arrow(7.5, 18, 6.25, 18)
    
    # 14. End
    create_box(2.5, 4.5, 2, 0.6, '🎯 Truth Synthesis\n& Interview Complete', 'end')
    create_arrow(2.5, 5.7, 2.5, 4.8)
    
    # Add decision matrix legend
    legend_x, legend_y = 0.5, 3
    ax.text(legend_x, legend_y + 1, '📋 DECISION TRIGGERS', fontsize=12, fontweight='bold')
    
    triggers = [
        ('🟢 LISTEN: Clear, detailed, consistent responses'),
        ('🟡 PAUSE: Processing, analyzing, strategizing'),  
        ('🔴 PUSH: Evasive, vague, contradictory responses')
    ]
    
    for i, trigger in enumerate(triggers):
        ax.text(legend_x, legend_y - i*0.3, trigger, fontsize=10)
    
    # Add escalation levels
    escalation_x = 6
    ax.text(escalation_x, legend_y + 1, '📈 ESCALATION LEVELS', fontsize=12, fontweight='bold')
    
    levels = [
        ('Level 1: 👀 Passive Monitoring'),
        ('Level 2: 🔍 Active Probing'),
        ('Level 3: 🕵️ Intensive Investigation'),
        ('Level 4: ⚡ Truth Extraction')
    ]
    
    for i, level in enumerate(levels):
        ax.text(escalation_x, legend_y - i*0.3, level, fontsize=10)
    
    plt.tight_layout()
    return fig

def create_decision_matrix():
    """Create a decision matrix visualization."""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Decision matrix data
    situations = ['Clear Answer', 'Vague Response', 'Minor Contradiction', 
                 'Major Contradiction', 'Evasion Detected', 'Truth Confirmed']
    
    confidence_levels = [0.9, 0.6, 0.6, 0.2, 0.2, 0.95]
    actions = ['Store & Continue', 'Request Details', 'Note & Monitor', 
              'Immediate Challenge', 'Targeted Probe', 'Document Truth']
    
    # Create heatmap-style visualization
    y_pos = np.arange(len(situations))
    
    # Color mapping based on confidence
    colors_map = ['red' if x < 0.4 else 'orange' if x < 0.7 else 'green' 
                  for x in confidence_levels]
    
    ax.barh(y_pos, confidence_levels, color=colors_map, alpha=0.7)
    
    # Add action labels
    for i, (conf, action) in enumerate(zip(confidence_levels, actions)):
        ax.text(conf + 0.02, i, f'{action}', va='center', fontsize=10, fontweight='bold')
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(situations)
    ax.set_xlabel('Confidence Level', fontsize=12, fontweight='bold')
    ax.set_title('🤖 AI Interviewer Decision Matrix', fontsize=16, fontweight='bold')
    ax.set_xlim(0, 1.2)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='High Risk (< 0.4)'),
        Patch(facecolor='orange', alpha=0.7, label='Medium Risk (0.4-0.7)'),
        Patch(facecolor='green', alpha=0.7, label='Low Risk (> 0.7)')
    ]
    ax.legend(handles=legend_elements, loc='lower right')
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Create and save the flowchart
    print("🧠 Generating Smart AI Interviewer Decision Flow...")
    
    # Main flowchart
    fig1 = create_ai_interviewer_flowchart()
    fig1.savefig('ai_interviewer_flowchart.png', dpi=300, bbox_inches='tight')
    print("✅ Flowchart saved as 'ai_interviewer_flowchart.png'")
    
    # Decision matrix
    fig2 = create_decision_matrix()
    fig2.savefig('ai_interviewer_decision_matrix.png', dpi=300, bbox_inches='tight')
    print("✅ Decision matrix saved as 'ai_interviewer_decision_matrix.png'")
    
    print("\n🎯 Bonus diagrams completed!")
    print("📊 Files created:")
    print("   - AI_Interviewer_Decision_Flow.md (Comprehensive markdown)")
    print("   - AI_Interviewer_Visual_Diagram.txt (ASCII art)")
    print("   - ai_interviewer_flowchart.png (Generated chart)")
    print("   - ai_interviewer_decision_matrix.png (Decision matrix)")
    
    # Show the plots
    plt.show()