"""
Generate comparison plots for ENTRO-CORE simulation results
"""

import matplotlib.pyplot as plt
import numpy as np
from simulation.system_dynamics import run_comparison, SimulationConfig

# Configure matplotlib for publication quality
plt.rcParams.update({
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'legend.fontsize': 10,
    'figure.dpi': 150,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight'
})


def generate_comparison_plots(results, save_dir="figures"):
    """Generate all comparison plots"""
    import os
    os.makedirs(save_dir, exist_ok=True)
    
    colors = {
        'uncontrolled': '#8a8078',
        'pid': '#3498db',
        'entro_core_linear': '#2ecc71',
        'entro_core_exp': '#e74c3c',
        'entro_core_quad': '#f39c12'
    }
    
    labels = {
        'uncontrolled': 'Uncontrolled',
        'pid': 'PID',
        'entro_core_linear': 'ENTRO-CORE (Linear)',
        'entro_core_exp': 'ENTRO-CORE (Exponential)',
        'entro_core_quad': 'ENTRO-CORE (Quadratic)'
    }
    
    # Figure 1: Ψ(t) over time
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    
    for name, result in results.items():
        ax1.plot(result.times, result.psi, label=labels[name], color=colors[name], linewidth=1.5)
    
    ax1.axhline(y=0, color='black', linestyle='--', linewidth=0.8, alpha=0.5)
    ax1.axhline(y=2.0, color='red', linestyle='--', linewidth=0.8, alpha=0.5, label='Ψ_c = 2.0')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Ψ (Entropy State)')
    ax1.set_title('ENTRO-CORE: Entropy State Evolution')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    fig1.savefig(f'{save_dir}/figure1_psi_comparison.png', dpi=300)
    fig1.savefig(f'{save_dir}/figure1_psi_comparison.pdf')
    print(f"✅ Saved: {save_dir}/figure1_psi_comparison.png")
    
    # Figure 2: Control signal u(t)
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    
    for name, result in results.items():
        if 'entro' in name:
            ax2.plot(result.times, result.u, label=labels[name], color=colors[name], linewidth=1.5)
    
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Control Signal u(t)')
    ax2.set_title('ENTRO-CORE: Control Signal Evolution')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.3)
    fig2.savefig(f'{save_dir}/figure2_control_signals.png', dpi=300)
    fig2.savefig(f'{save_dir}/figure2_control_signals.pdf')
    print(f"✅ Saved: {save_dir}/figure2_control_signals.png")
    
    # Figure 3: Phase space (Ψ vs dΨ/dt)
    fig3, ax3 = plt.subplots(figsize=(10, 8))
    
    for name, result in results.items():
        ax3.plot(result.psi, result.dpsi, label=labels[name], color=colors[name], linewidth=1.0, alpha=0.8)
    
    ax3.axhline(y=0, color='black', linestyle='--', linewidth=0.5, alpha=0.3)
    ax3.axvline(x=0, color='black', linestyle='--', linewidth=0.5, alpha=0.3)
    ax3.set_xlabel('Ψ (Entropy State)')
    ax3.set_ylabel('dΨ/dt (Entropy Velocity)')
    ax3.set_title('ENTRO-CORE: Phase Space Trajectories')
    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.3)
    fig3.savefig(f'{save_dir}/figure3_phase_space.png', dpi=300)
    fig3.savefig(f'{save_dir}/figure3_phase_space.pdf')
    print(f"✅ Saved: {save_dir}/figure3_phase_space.png")
    
    # Figure 4: Metrics bar chart
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    
    controllers = ['Uncontrolled', 'PID', 'ENTRO-CORE\n(Linear)', 'ENTRO-CORE\n(Exponential)', 'ENTRO-CORE\n(Quadratic)']
    iae_values = [
        results['uncontrolled'].metrics['IAE'],
        results['pid'].metrics['IAE'],
        results['entro_core_linear'].metrics['IAE'],
        results['entro_core_exp'].metrics['IAE'],
        results['entro_core_quad'].metrics['IAE']
    ]
    
    bars = ax4.bar(controllers, iae_values, color=['#8a8078', '#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
    ax4.set_ylabel('IAE (Integral Absolute Error)')
    ax4.set_title('Performance Comparison: IAE Metric')
    
    for bar, val in zip(bars, iae_values):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, f'{val:.1f}', ha='center', va='bottom', fontsize=10)
    
    fig4.savefig(f'{save_dir}/figure4_iae_comparison.png', dpi=300)
    fig4.savefig(f'{save_dir}/figure4_iae_comparison.pdf')
    print(f"✅ Saved: {save_dir}/figure4_iae_comparison.png")
    
    plt.close('all')
    print("\n✅ All figures generated successfully!")


def generate_publication_figures():
    """Generate all figures for publication"""
    print("=" * 60)
    print("Generating Publication-Quality Figures")
    print("=" * 60)
    print()
    
    config = SimulationConfig(duration=50.0, dt=0.1)
    results = run_comparison(config)
    
    print()
    generate_comparison_plots(results)
    
    return results


if __name__ == "__main__":
    results = generate_publication_figures()
