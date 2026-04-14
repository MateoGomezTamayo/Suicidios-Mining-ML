"""
Script de demostración: Predicciones con coeficientes epidemiológicos actualizados
Casos: Bajo, Medio, Alto sin necesidad de cargar modelo
"""
import numpy as np

print("\n" + "="*70)
print("DEMOSTRACIÓN: PREDICCIONES CON COEFICIENTES EPIDEMIOLÓGICOS")
print("="*70)

def predecir_caso(nombre_caso, tran_dep, trast_p, trast_b, esquizo, antec_t,
                  idea_s, plan_s, prob_raw_base, prob_raw_prio):
    """Simular predicción basada en probabilidades y severidad clínica"""
    
    # Cálculo del puntaje con COEFICIENTES ACTUALIZADOS
    puntaje_manual = int(3*tran_dep + 3*trast_p + 4*trast_b + 4*esquizo + 3*antec_t)
    combo_critico = int(tran_dep == 1 and plan_s == 1 and idea_s == 1)
    
    # Umbrales dinámicos
    umbral_base = 0.03417937
    factor_severidad = max(0.0, min(1.0, puntaje_manual / 17.0))
    umbral_modelo = max(1e-6, umbral_base * (1.0 - 0.98 * factor_severidad))
    
    # Predicción modelo CRUDO
    pred_modelo_crudo = int(prob_raw_prio >= umbral_base)
    clase_modelo_crudo = "PRIORITARIO" if pred_modelo_crudo == 1 else "BASE"
    
    # Score ajustado
    score_modelo_ajustado = min(1.0, float(prob_raw_prio) + 0.08 * factor_severidad + 0.04 * combo_critico)
    pred_modelo = int(score_modelo_ajustado >= umbral_modelo)
    clase_modelo = "PRIORITARIO" if pred_modelo == 1 else "BASE"
    
    # Regla clínica
    regla_clinica = (puntaje_manual >= 9) or (tran_dep == 1 and plan_s == 1 and idea_s == 1)
    pred_manual = int(pred_modelo == 1 or regla_clinica)
    clase_final = "PRIORITARIO" if pred_manual == 1 else "BASE"
    
    # Motivo
    if regla_clinica and pred_modelo == 0:
        motivo = "Regla clínica de urgencia activada"
    elif regla_clinica and pred_modelo == 1:
        motivo = "Modelo + regla clínica coinciden"
    else:
        motivo = "Decisión basada en severidad del modelo"
    
    # Salida
    print(f"\n{'─'*70}")
    print(f"CASO: {nombre_caso.upper()}")
    print(f"{'─'*70}")
    print(f"\n[1] PROBABILIDADES CRUDAS")
    print(f"    Prob. Base       : {prob_raw_base:.2%} ({prob_raw_base:.8f})")
    print(f"    Prob. Prioritario: {prob_raw_prio:.2%} ({prob_raw_prio:.8f})")
    print(f"    Predicción cruda : {clase_modelo_crudo}")
    
    print(f"\n[2] AJUSTE POR SEVERIDAD CLÍNICA")
    print(f"    Puntaje trastornos      : {puntaje_manual}/17")
    print(f"    Factor severidad        : {factor_severidad:.2%}")
    print(f"    Score ajustado          : {score_modelo_ajustado:.8f}")
    print(f"    Umbral dinámico         : {umbral_modelo:.8f}")
    print(f"    Predicción ajustada     : {clase_modelo}")
    
    print(f"\n[3] REGLA CLÍNICA DE URGENCIA")
    print(f"    Puntaje >= 9            : {puntaje_manual >= 9} ({puntaje_manual}/17)")
    print(f"    Depre + Plan + Idea     : {combo_critico == 1}")
    print(f"    Regla clínica           : {'ACTIVA ✓' if regla_clinica else 'NO ACTIVA'}")
    
    print(f"\n{'═'*70}")
    print(f"║ PREDICCIÓN FINAL: {clase_final:26} ║")
    print(f"║ Justificación: {motivo:43} ║")
    print(f"{'═'*70}")

# CASO 1: SIN TRASTORNOS (bajo riesgo)
# Trastornos: ninguno | Idea/Plan: no | Prob modelo: casi BASE puro
predecir_caso(
    "Bajo Riesgo", 
    tran_dep=0, trast_p=0, trast_b=0, esquizo=0, antec_t=0,
    idea_s=0, plan_s=0,
    prob_raw_base=0.99999, prob_raw_prio=0.00001
)

# CASO 2: TRASTORNOS MODERADOS (riesgo medio)
# Trastornos: depresión + antecedente | Idea: sí, Plan: no | Prob modelo: bajo
predecir_caso(
    "Riesgo Medio",
    tran_dep=1, trast_p=0, trast_b=0, esquizo=0, antec_t=1,
    idea_s=1, plan_s=0,
    prob_raw_base=0.95, prob_raw_prio=0.05
)

# CASO 3: MÚLTIPLES TRASTORNOS (riesgo alto)
# Trastornos: todos | Idea: sí, Plan: sí | Prob modelo: bajo pero muchos trastornos
predecir_caso(
    "Riesgo Alto",
    tran_dep=1, trast_p=1, trast_b=1, esquizo=1, antec_t=1,
    idea_s=1, plan_s=1,
    prob_raw_base=0.95, prob_raw_prio=0.05
)

print("\n" + "="*70)
print("EXPLICACIÓN: Por qué el modelo Crudo predice BASE pero el FINAL es PRIORITARIO")
print("="*70)
print("""
En casos con MUCHOS TRASTORNOS psiquiátricos:

1. El modelo crudo (basado en probabilidades históricas) predice BASE porque:
   → Pocos PRIORITARIOS históricos = modelo "conservador"
   
2. PERO aplicamos AJUSTES CLÍNICOS:
   → Si puntaje >= 9/17 (severidad alta) → aumentamos la sensibilidad
   → Si hay COMBO CRÍTICO (depresión + plan + idea) → activamos urgencia
   
3. RESULTADO: Modelo AJUSTADO + REGLA CLÍNICA = PRIORITARIO
   → Refleja la realidad clínica (muchos trastornos = alto riesgo)
   
✓ CONCLUSIÓN: No es confusión, es que el modelo aprende a ser CLÍNICAMENTE INTELIGENTE
""")
