export function errorMessageToString(errors) {
    let errorMessage = 'Неизвестная ошибка';
    if (Array.isArray(errors) && errors.length > 0) {
        errorMessage = errors.join('<br />')
    } else if (typeof(errors) === 'string' && errors.length > 0) {
        errorMessage = errors;
    } else if (typeof(errors) === 'object') {
        let error_messages = [];
        for (const prop in errors) {
          if (errors.hasOwnProperty(prop)) {
              error_messages.push(`${prop}: ${errors[prop]}`);
          }
        }
        errorMessage = error_messages.join('<br />');
    }
    return errorMessage
}
