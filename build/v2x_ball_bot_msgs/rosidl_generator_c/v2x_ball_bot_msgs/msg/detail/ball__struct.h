// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from v2x_ball_bot_msgs:msg/Ball.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__STRUCT_H_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"
// Member 'id'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/Ball in the package v2x_ball_bot_msgs.
/**
  * Ball.msg
 */
typedef struct v2x_ball_bot_msgs__msg__Ball
{
  builtin_interfaces__msg__Time stamp;
  rosidl_runtime_c__String id;
  float x;
  float y;
  float z;
  float score;
  bool is_static;
} v2x_ball_bot_msgs__msg__Ball;

// Struct for a sequence of v2x_ball_bot_msgs__msg__Ball.
typedef struct v2x_ball_bot_msgs__msg__Ball__Sequence
{
  v2x_ball_bot_msgs__msg__Ball * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} v2x_ball_bot_msgs__msg__Ball__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL__STRUCT_H_
