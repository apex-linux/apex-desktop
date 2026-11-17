// Implements https://google.github.io/styleguide/jsguide.html for the GJS
// code in this repository. The Google guide wins where a rule disagrees.

import js from '@eslint/js';
import stylistic from '@stylistic/eslint-plugin';
import globals from 'globals';

export default [
  {
    ignores: ['node_modules/', 'build/', '.venv/'],
  },
  js.configs.recommended,
  {
    files: ['**/*.js'],
    languageOptions: {
      ecmaVersion: 2024,
      sourceType: 'module',
      globals: {
        ...globals.node,
      },
    },
    plugins: {'@stylistic': stylistic},
    rules: {
      '@stylistic/arrow-parens': ['error', 'always'],
      '@stylistic/brace-style': ['error', '1tbs'],
      '@stylistic/comma-dangle': ['error', 'always-multiline'],
      '@stylistic/comma-spacing': 'error',
      '@stylistic/eol-last': 'error',
      '@stylistic/indent': ['error', 2, {
        CallExpression: {arguments: 2},
        FunctionDeclaration: {parameters: 2},
        FunctionExpression: {parameters: 2},
        MemberExpression: 2,
        SwitchCase: 1,
      }],
      '@stylistic/key-spacing': 'error',
      '@stylistic/keyword-spacing': 'error',
      '@stylistic/list-style': ['error', {
        singleLine: {spacing: 'never'},
        // Google style wraps arguments with a continuation indent, not one
        // argument per line, so parentheses are left to max-len and indent.
        overrides: {'{}': {singleLine: {spacing: 'never'}}, '()': 'off'},
      }],
      '@stylistic/max-len': ['error', {
        code: 80,
        ignoreUrls: true,
        ignorePattern: '^import\\s.+\\sfrom\\s.+;$',
      }],
      '@stylistic/no-multi-spaces': 'error',
      '@stylistic/no-tabs': 'error',
      '@stylistic/no-trailing-spaces': 'error',
      '@stylistic/operator-linebreak': ['error', 'after'],
      '@stylistic/quotes': ['error', 'single', {
        allowTemplateLiterals: 'always',
      }],
      '@stylistic/semi': ['error', 'always'],
      '@stylistic/space-before-blocks': 'error',
      '@stylistic/space-before-function-paren': ['error', {
        anonymous: 'never',
        named: 'never',
        asyncArrow: 'always',
      }],
      'camelcase': ['error', {properties: 'never'}],
      'curly': ['error', 'multi-line'],
      'new-cap': 'error',
      'no-var': 'error',
      'prefer-const': ['error', {destructuring: 'all'}],
      'prefer-rest-params': 'error',
      'prefer-spread': 'error',
    },
  },
  {
    // GNOME Shell extensions run in GJS, which has its own globals.
    files: ['extension/**/*.js'],
    languageOptions: {
      globals: {
        global: 'readonly',
        log: 'readonly',
        logError: 'readonly',
      },
    },
  },
];
