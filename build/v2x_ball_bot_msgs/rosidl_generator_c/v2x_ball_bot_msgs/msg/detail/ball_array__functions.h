// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from v2x_ball_bot_msgs:msg/BallArray.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__FUNCTIONS_H_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "v2x_ball_bot_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "v2x_ball_bot_msgs/msg/detail/ball_array__struct.h"

/// Initialize msg/BallArray message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * v2x_ball_bot_msgs__msg__BallArray
 * )) before or use
 * v2x_ball_bot_msgs__msg__BallArray__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
bool
v2x_ball_bot_msgs__msg__BallArray__init(v2x_ball_bot_msgs__msg__BallArray * msg);

/// Finalize msg/BallArray message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
void
v2x_ball_bot_msgs__msg__BallArray__fini(v2x_ball_bot_msgs__msg__BallArray * msg);

/// Create msg/BallArray message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * v2x_ball_bot_msgs__msg__BallArray__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
v2x_ball_bot_msgs__msg__BallArray *
v2x_ball_bot_msgs__msg__BallArray__create();

/// Destroy msg/BallArray message.
/**
 * It calls
 * v2x_ball_bot_msgs__msg__BallArray__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
void
v2x_ball_bot_msgs__msg__BallArray__destroy(v2x_ball_bot_msgs__msg__BallArray * msg);

/// Check for msg/BallArray message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
bool
v2x_ball_bot_msgs__msg__BallArray__are_equal(const v2x_ball_bot_msgs__msg__BallArray * lhs, const v2x_ball_bot_msgs__msg__BallArray * rhs);

/// Copy a msg/BallArray message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
bool
v2x_ball_bot_msgs__msg__BallArray__copy(
  const v2x_ball_bot_msgs__msg__BallArray * input,
  v2x_ball_bot_msgs__msg__BallArray * output);

/// Initialize array of msg/BallArray messages.
/**
 * It allocates the memory for the number of elements and calls
 * v2x_ball_bot_msgs__msg__BallArray__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
bool
v2x_ball_bot_msgs__msg__BallArray__Sequence__init(v2x_ball_bot_msgs__msg__BallArray__Sequence * array, size_t size);

/// Finalize array of msg/BallArray messages.
/**
 * It calls
 * v2x_ball_bot_msgs__msg__BallArray__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
void
v2x_ball_bot_msgs__msg__BallArray__Sequence__fini(v2x_ball_bot_msgs__msg__BallArray__Sequence * array);

/// Create array of msg/BallArray messages.
/**
 * It allocates the memory for the array and calls
 * v2x_ball_bot_msgs__msg__BallArray__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
v2x_ball_bot_msgs__msg__BallArray__Sequence *
v2x_ball_bot_msgs__msg__BallArray__Sequence__create(size_t size);

/// Destroy array of msg/BallArray messages.
/**
 * It calls
 * v2x_ball_bot_msgs__msg__BallArray__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
void
v2x_ball_bot_msgs__msg__BallArray__Sequence__destroy(v2x_ball_bot_msgs__msg__BallArray__Sequence * array);

/// Check for msg/BallArray message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
bool
v2x_ball_bot_msgs__msg__BallArray__Sequence__are_equal(const v2x_ball_bot_msgs__msg__BallArray__Sequence * lhs, const v2x_ball_bot_msgs__msg__BallArray__Sequence * rhs);

/// Copy an array of msg/BallArray messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_v2x_ball_bot_msgs
bool
v2x_ball_bot_msgs__msg__BallArray__Sequence__copy(
  const v2x_ball_bot_msgs__msg__BallArray__Sequence * input,
  v2x_ball_bot_msgs__msg__BallArray__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_ARRAY__FUNCTIONS_H_
