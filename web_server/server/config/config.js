yaml = require('js-yaml');
fs   = require('fs');
var path = require('path');

// Get document, or throw exception on error

const load_config = function() {
  return yaml.safeLoad(fs.readFileSync(path.join(__dirname, '../../../config/config.yml'), 'utf8'));
}

exports.load_config = load_config
