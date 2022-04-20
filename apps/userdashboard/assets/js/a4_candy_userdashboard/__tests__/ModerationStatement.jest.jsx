import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import { ModerationStatement } from '../ModerationStatement'

test('ModerationStatement with optimal values', () => {
  const mockProps = {
    statement: 'test statement',
    last_edit: '20. April 2022, 3 PM',
    pk: 1
  }
  render(<ModerationStatement statement={mockProps} />)
  const statement = screen.getByText('test statement')
  expect(statement).toBeTruthy()
})

test('ModerationStatement onDelete', () => {
  const mockProps = {
    statement: 'test statement',
    last_edit: '20. April 2022, 3 PM',
    pk: 1
  }
  const mockOnDelete = jest.fn()
  render(
    <ModerationStatement
      statement={mockProps}
      onDelete={mockOnDelete}
    />)
  const deleteButton = document.querySelector('li button')
  fireEvent.click(deleteButton)
  expect(mockOnDelete).toHaveBeenCalled()
})
