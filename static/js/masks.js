// ────────────────────────────────────────────────────────────────────
// MASCARAS (jQuery Mask Plugin)
// ────────────────────────────────────────────────────────────────────
$(function () {
  // Garante que o jQuery está carregado
  if (typeof $ !== 'undefined' && $.fn.mask) {

    // Inicializa máscaras baseadas no atributo data-masks
    $('input[data-masks="cpf"]').mask('000.000.000-00');
    $('input[data-masks="cnpj"]').mask('00.000.000/0000-00');
    $('input[data-masks="cep"]').mask('00.000-000');
    $('input[data-masks="telefone"]').mask('(00) 0000-00009'); // 8 ou 9 dígitos

    // Máscara dinâmica para telefone (fixo ou celular)
    var PhoneMaskBehavior = function (val) {
      return val.replace(/\D/g, '').length === 11 ? '(00) 00000-0000' : '(00) 0000-00009';
    },
      spOptions = {
        onKeyPress: function (val, e, field, options) {
          field.mask(PhoneMaskBehavior.apply({}, arguments), options);
        }
      };

    $('input[data-masks="celular"]').mask(PhoneMaskBehavior, spOptions);

    $('input[data-masks="data"]').mask('00/00/0000');
    $('input[data-masks="hora"]').mask('00:00');
    $('input[data-masks="moeda"]').mask('#.##0,00', { reverse: true });

    console.log('Máscaras inicializadas com sucesso.');
  } else {
    console.warn('jQuery ou jQuery Mask Plugin não encontrados.');
  }
});
