# Usar Colab Notebook
- Vms usar ele para tentar encontrar uma lacuna de pesquisa na área.
- até o momento não tenho nenhuma ideia.

# Usar google colab também para terminar referencial teórico.
- Vms usar google colab para terminar referencial teórico.


Algoritmo: Certified_Quantization_SMT(N, I, O, Bl, Bu)
  // N: Rede Neural, I: Região de Entrada, O: Região de Saída, Bl/Bu: Bits Fracionários Mín/Máx

  1. Aplique DeepPoly em N w.r.t. I para obter elementos abstratos {A^{2i} | 1 ≤ i ≤ d};  // Igual ao original

  2. Defina P^{2d} = O e �N = N;  // Pré-imagem inicial na saída

  3. Para i = d-1 até 1 faça:  // Etapa Backward: Computa Pré-Imagens
     // MUDANÇA: Em vez de MILP, use SMT para otimizar χ e propagar P^{2i+2}
     P^{2i} = UnderPreImage_SMT(N, A^{2i}, P^{2i+2});
     // UnderPreImage_SMT: Codifique constraints lineares (afim + ReLU via big-M) em SMT.
     // Maximize χ s.t. N_{[2i+1:2i+2]}(T^{2i}) ⊆ P^{2i+2} (template T escalado por χ).
     // Se SAT, extraia modelo; se UNSAT, ajuste χ via binary search.

  4. Para i = 1 até d faça:  // Etapa Forward: Quantização
     ξ_i = ⊥;  // Configuração inicial nula
     I_bit = bits mínimos para parte inteira de W^{2i} e b^{2i} sem overflow;  // Igual

     Para F = Bl até Bu faça:
       // Quantize W^{2i}, b^{2i} w.r.t. ˇξ_i = <F + I_bit, F> em �N para obter �N^{2i};
       Aplique DeepPoly em �N^{2i}_{[1:2i]} w.r.t. I para obter �A^{2i};  // Pode substituir por SMT para verificação exata

       // MUDANÇA: Verifique inclusão com SMT: Codifique γ(�A^{2i}) ⊆ P^{2i} como fórmula SMT.
       // Adicione constraints: exists x em �A^{2i} tal que x ∉ P^{2i}? Se UNSAT, inclusão holds.
       Se γ(�A^{2i}) ⊆ P^{2i} (via SMT check) então:
         ξ_i = ˇξ_i; Atualize �N = �N^{2i};  // Aceita e prossegue
         Quebre o loop

     Se ξ_i == ⊥ então retorne UNKNOWN  // Falhou

  5. Retorne Ξ = {ξ_1, ..., ξ_d};  // Estratégia de quantização certificada



# Ideias

Vms