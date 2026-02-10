// ────────────────────────────────────────────────────────────────────
// Função Auxiliar para Mostrar Alertas Bootstrap
// ────────────────────────────────────────────────────────────────────
function showAlert(message, type) {
  const alertContainer = document.getElementById('alert-container');
  if (!alertContainer) return;

  const wrapper = document.createElement('div');
  wrapper.innerHTML = [
    `<div class="alert alert-${type} alert-dismissible fade show" role="alert">`,
    `   <div>${message}</div>`,
    '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
    '</div>'
  ].join('');

  alertContainer.append(wrapper);

  // Auto-remove após 5 segundos (opcional, bom para UX)
  setTimeout(() => {
    const alert = wrapper.firstElementChild;
    if (alert) {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }
  }, 5000);
}

// ────────────────────────────────────────────────────────────────────
// Inicializador de Busca de CNPJ Reutilizável
// ────────────────────────────────────────────────────────────────────
function initCNPJSearch(config) {
  const btnBuscarCNPJ = document.getElementById(config.btnId);
  const inputCNPJ = document.getElementById(config.inputId);

  // Mensagens padrão (podem ser sobrescritas via config.messages)
  const messages = {
    invalidCNPJ: 'Por favor, digite um CNPJ válido com 14 dígitos.',
    searching: 'Consultando Receita Federal...',
    success: 'Dados encontrados com sucesso!',
    errorDefault: 'Erro ao consultar CNPJ.',
    ...config.messages
  };

  if (btnBuscarCNPJ && inputCNPJ) {
    btnBuscarCNPJ.addEventListener('click', function () {
      // Remove caracteres não numéricos
      let cnpj = inputCNPJ.value.replace(/\D/g, '');

      if (cnpj.length !== 14) {
        showAlert(messages.invalidCNPJ, 'warning');
        return;
      }

      // Salva o conteúdo original do botão
      const originalBtnContent = btnBuscarCNPJ.innerHTML;

      // Bloqueio de UI
      btnBuscarCNPJ.disabled = true;
      btnBuscarCNPJ.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

      // Feedback
      showAlert(messages.searching, 'info');

      // Gera URL
      const url = config.apiUrlPattern.replace('00000000000000', cnpj);

      fetch(url)
        .then(function (response) {
          if (!response.ok) {
            return response.json().then(function (err) { throw err; });
          }
          return response.json();
        })
        .then(function (data) {
          // Sucesso
          showAlert(messages.success, 'success');

          // Função auxiliar para preencher e disparar máscaras
          const setField = (fieldId, value) => {
            if (!fieldId) return; // Se não houver ID mapeado, ignora
            const el = document.getElementById(fieldId);
            if (el && value) {
              el.value = value;
              el.dispatchEvent(new Event('input', { bubbles: true }));
              if (typeof $ !== 'undefined') {
                $(el).trigger('input');
              }
            }
          };

          // Itera sobre o mapa de campos e preenche
          // Formato fieldsMap: { 'api_key': 'dom_id' }
          for (const [apiKey, fieldId] of Object.entries(config.fieldsMap)) {
            let value = data[apiKey];

            // Tratamentos específicos
            if (apiKey === 'endereco_cep' && value) {
              value = value.replace(/\D/g, ''); // Limpa CEP p/ máscara
            }

            if (value) {
              setField(fieldId, value);
            }
          }

        })
        .catch(function (error) {
          // Erro
          const errorMsg = error.erro || messages.errorDefault;
          showAlert(errorMsg, 'danger');
        })
        .finally(function () {
          // Restaura UI Original
          btnBuscarCNPJ.disabled = false;
          btnBuscarCNPJ.innerHTML = originalBtnContent;
        });
    });
  }
}

// ────────────────────────────────────────────────────────────────────
// Inicializador de Busca de CEP Reutilizável
// ────────────────────────────────────────────────────────────────────
function initCEPSearch(config) {
  const btnBuscarCEP = document.getElementById(config.btnId);
  const inputCEP = document.getElementById(config.inputId);

  const messages = {
    invalidCEP: 'Por favor, digite um CEP válido com 8 dígitos.',
    searching: 'Buscando CEP...',
    success: 'Endereço encontrado!',
    errorDefault: 'Erro ao buscar CEP.',
    ...config.messages
  };

  if (btnBuscarCEP && inputCEP) {
    btnBuscarCEP.addEventListener('click', function () {
      let cep = inputCEP.value.replace(/\D/g, '');

      if (cep.length !== 8) {
        showAlert(messages.invalidCEP, 'warning');
        return;
      }

      const originalBtnContent = btnBuscarCEP.innerHTML;

      // UI Loading
      btnBuscarCEP.disabled = true;
      btnBuscarCEP.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

      showAlert(messages.searching, 'info');

      const url = config.apiUrlPattern.replace('00000000', cep);

      fetch(url)
        .then(function (response) {
          if (!response.ok) {
            return response.json().then(function (err) { throw err; });
          }
          return response.json();
        })
        .then(function (data) {
          showAlert(messages.success, 'success');

          // Função auxiliar para preencher
          const setField = (fieldId, value) => {
            if (!fieldId) return;
            const el = document.getElementById(fieldId);
            if (el && value) {
              el.value = value;
              el.dispatchEvent(new Event('input', { bubbles: true }));
              if (typeof $ !== 'undefined') {
                $(el).trigger('input');
              }
            }
          };

          for (const [apiKey, fieldId] of Object.entries(config.fieldsMap)) {
            let value = data[apiKey];
            if (value) {
              setField(fieldId, value);
            }
          }
        })
        .catch(function (error) {
          const errorMsg = error.erro || messages.errorDefault;
          showAlert(errorMsg, 'danger');
        })
        .finally(function () {
          btnBuscarCEP.disabled = false;
          btnBuscarCEP.innerHTML = originalBtnContent;
        });
    });
  }
}

// ────────────────────────────────────────────────────────────────────
// Inicializador de Tooltips do Bootstrap e Controle de Tela Cheia
// ────────────────────────────────────────────────────────────────────
$(document).ready(function () {
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  initFullscreenControl();
});

// ────────────────────────────────────────────────────────────────────
// Controle de Tela Cheia
// ────────────────────────────────────────────────────────────────────
function initFullscreenControl() {
  const toggleBtn = document.getElementById('maximizeToggle');
  if (!toggleBtn) return;

  // Ícones (SVG ou classes BS Icons)
  // Como o Django renderiza SVGs com {% bs_icon %}, vamos manipular o HTML interno ou classes se possível.
  // Simplificando: vamos alternar classes se for <i> ou substituir o HTML se for SVG complexo.
  // O mais seguro neste projeto (que usa {% bs_icon %}) é trocar o innerHTML com a string do ícone novo, 
  // mas sem o server-side rendering do Django aqui no JS, precisamos do HTML do ícone clientside.
  // Vamos usar classes do bootstrap-icons (font) se disponível, ou SVGs inline genéricos.
  // O user usa {% bs_icon 'arrows-fullscreen' %}.

  const iconMaximize = '<i class="bi bi-arrows-fullscreen"></i>'; // Fallback se usar fonte
  const iconMinimize = '<i class="bi bi-fullscreen-exit"></i>';

  // MELHOR ABORDAGEM: Manter o SVG original e apenas trocar se necessário, 
  // mas como não temos os SVGs exatos do helper django aqui, 
  // vamos assumir que bootstrap-icons.css está carregado (padrão) ou usar SVGs padrão do Bootstrap.

  // SVGs do Bootstrap 1.11
  const svgMaximize = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrows-fullscreen" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M5.828 10.172a.5.5 0 0 0-.707 0l-4.096 4.096V11.5a.5.5 0 0 0-1 0v3.975a.5.5 0 0 0 .5.5H4.5a.5.5 0 0 0 0-1H1.732l4.096-4.096a.5.5 0 0 0 0-.707zm4.344 0a.5.5 0 0 1 .707 0l4.096 4.096V11.5a.5.5 0 1 1 1 0v3.975a.5.5 0 0 1-.5.5H11.5a.5.5 0 0 1 0-1h2.768l-4.096-4.096a.5.5 0 0 1 0-.707zm0-4.344a.5.5 0 0 0 .707 0l4.096-4.096V4.5a.5.5 0 1 0 1 0V.525a.5.5 0 0 0-.5-.5H11.5a.5.5 0 0 0 0 1h2.768l-4.096 4.096a.5.5 0 0 0 0 .707zm-4.344 0a.5.5 0 0 1-.707 0L1.025 1.732V4.5a.5.5 0 0 1-1 0V.525a.5.5 0 0 1 .5-.5H4.5a.5.5 0 0 1 0 1H1.732l4.096 4.096a.5.5 0 0 1 0 .707z"/>
</svg>`;

  const svgMinimize = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-fullscreen-exit" viewBox="0 0 16 16">
  <path d="M5.5 0a.5.5 0 0 1 .5.5v4A1.5 1.5 0 0 1 4.5 6h-4a.5.5 0 0 1 0-1h4a.5.5 0 0 0 .5-.5v-4a.5.5 0 0 1 .5-.5zm5 0a.5.5 0 0 1 .5.5v4a.5.5 0 0 0 .5.5h4a.5.5 0 0 1 0 1h-4A1.5 1.5 0 0 1 10 4.5v-4a.5.5 0 0 1 .5-.5zM0 10.5a.5.5 0 0 1 .5-.5h4A1.5 1.5 0 0 1 6 11.5v4a.5.5 0 0 1-1 0v-4a.5.5 0 0 0-.5-.5h-4a.5.5 0 0 1-.5-.5zm10 1a1.5 1.5 0 0 1 1.5-1.5h4a.5.5 0 0 1 0 1h-4a.5.5 0 0 0-.5.5v4a.5.5 0 0 1-1 0v-4z"/>
</svg>`;

  function updateIcon(isFullscreen) {
    toggleBtn.innerHTML = isFullscreen ? svgMinimize : svgMaximize;
    // Opcional: Adicionar tooltip se necessário
    toggleBtn.setAttribute('title', isFullscreen ? 'Restaurar Tela' : 'Tela Cheia');
  }

  toggleBtn.addEventListener('click', function () {
    if (!document.fullscreenElement) {
      document.documentElement.requestFullscreen().catch(err => {
        console.log(`Erro ao ativar tela cheia: ${err.message}`);
      });
    } else {
      if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    }
  });

  // Ouve mudanças (ESC, F11, etc)
  document.addEventListener('fullscreenchange', function () {
    const isFullscreen = !!document.fullscreenElement;
    updateIcon(isFullscreen);
  });
}
