vim.keymap.set('n', '<C-l>', ':bn<CR>')
vim.keymap.set('n', '<C-h>', ':bp<CR>')

-- Telescope
local builtin = require('telescope.builtin')
vim.keymap.set('n', '<leader>ff', builtin.find_files, { desc = 'Telecscope: find files' })
vim.keymap.set('n', '<leader>fg', builtin.live_grep,  { desc = 'Telecscope: live grep' })
