import React from 'react'
import { render, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ModerationNotificationActionsBar } from '../ModerationNotificationActionsBar'

test('Unread has three buttons', () => {
  const mockUnread = true
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
    />
  )
  const buttons = tree.container.querySelectorAll('button')
  expect(buttons.length).toBe(3)
})

test('Unread with reply button changing to edit button', () => {
  const mockUnread = true
  const mockEditing = true
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
      isEditing={mockEditing}
    />
  )
  const editIcon = tree.container.querySelector('.fa-pen')
  expect(editIcon).toBeTruthy()
})

test('Unread with highlight button disabled', () => {
  const mockUnread = true
  const mockBlocked = true
  const mockHighlighted = false
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
      isBlocked={mockBlocked}
      isHighlighted={mockHighlighted}
    />
  )
  const button =
    tree.container.querySelector('#moderation-notification-actions-bar-button-highlight')
  expect(button).toBeDisabled()
})

test('Unread with blocked button disabled', () => {
  const mockUnread = true
  const mockBlocked = false
  const mockHighlighted = true
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
      isBlocked={mockBlocked}
      isHighlighted={mockHighlighted}
    />
  )
  const button =
    tree.container.querySelector('#moderation-notification-actions-bar-button-block')
  expect(button).toBeDisabled()
})

test('Unread is highlighted', () => {
  const mockUnread = true
  const mockHighlighted = true
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
      isHighlighted={mockHighlighted}
    />
  )
  const buttons = tree.container.querySelectorAll('button')
  expect(buttons.length).toBe(3)
})

test('Unread clicks: reply --> highlight --> block', () => {
  const mockUnread = true
  const mockDisabled = false
  const mockBlocked = false
  const mockHighlighted = false
  const mockToggleFn = jest.fn()
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
      isDisabled={mockDisabled}
      isBlocked={mockBlocked}
      isHighlighted={mockHighlighted}
      onToggleForm={mockToggleFn}
      onToggleBlock={mockToggleFn}
      onToggleHighlight={mockToggleFn}
    />
  )
  const replyButton =
    tree.container.querySelector('#moderation-notification-actions-bar-button-reply')
  const highlightButton =
    tree.container.querySelector('#moderation-notification-actions-bar-button-highlight')
  const blockButton =
    tree.container.querySelector('#moderation-notification-actions-bar-button-block')

  fireEvent.click(replyButton)
  fireEvent.click(highlightButton)
  fireEvent.click(blockButton)
  expect(mockToggleFn).toHaveBeenCalledTimes(3)
})

test('Read has one button', () => {
  const mockUnread = false
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
    />
  )
  const buttons = tree.container.querySelectorAll('button')
  expect(buttons.length).toBe(1)
})

test('Read blocked shows blocked text', () => {
  const mockUnread = false
  const mockBlocked = true
  const tree = render(
    <ModerationNotificationActionsBar
      isUnread={mockUnread}
      isBlocked={mockBlocked}
    />
  )
  const blockedTextDiv = tree.container.querySelector('.fw-bold')
  expect(blockedTextDiv).toBeTruthy()
})
