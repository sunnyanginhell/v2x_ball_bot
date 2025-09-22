// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from v2x_ball_bot_msgs:msg/BallPixel.idl
// generated code does not contain a copyright notice

#ifndef V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__STRUCT_H_
#define V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/BallPixel in the package v2x_ball_bot_msgs.
typedef struct v2x_ball_bot_msgs__msg__BallPixel
{
  int32_t u;
  int32_t v;
} v2x_ball_bot_msgs__msg__BallPixel;

// Struct for a sequence of v2x_ball_bot_msgs__msg__BallPixel.
typedef struct v2x_ball_bot_msgs__msg__BallPixel__Sequence
{
  v2x_ball_bot_msgs__msg__BallPixel * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} v2x_ball_bot_msgs__msg__BallPixel__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // V2X_BALL_BOT_MSGS__MSG__DETAIL__BALL_PIXEL__STRUCT_H_
